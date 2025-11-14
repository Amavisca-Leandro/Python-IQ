"""
Metrics Reporter for generating quality dashboards and reports.

This module provides functionality to generate comprehensive reports including:
- Coverage metrics
- Historical trends
- ROI calculations
- Quality dashboards
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from .metrics_collector import MetricsCollector, get_metrics_collector


@dataclass
class CoverageMetrics:
    """Test coverage metrics."""
    total_endpoints: int
    covered_endpoints: int
    coverage_percentage: float
    uncovered_endpoints: List[str]
    test_count_by_endpoint: Dict[str, int]


@dataclass
class TrendData:
    """Historical trend data."""
    period: str
    pass_rate_trend: List[float]
    duration_trend: List[float]
    test_count_trend: List[int]
    dates: List[str]


@dataclass
class ROIMetrics:
    """Return on Investment metrics for test automation."""
    total_test_runs: int
    total_time_saved_hours: float
    manual_test_time_hours: float
    automated_test_time_hours: float
    time_savings_percentage: float
    estimated_cost_savings: float
    defects_found: int
    defects_prevented: int


class MetricsReporter:
    """Generates quality reports and dashboards from collected metrics."""
    
    def __init__(self, metrics_collector: Optional[MetricsCollector] = None):
        """
        Initialize the metrics reporter.
        
        Args:
            metrics_collector: MetricsCollector instance (uses global if None)
        """
        self.collector = metrics_collector or get_metrics_collector()
        self.reports_dir = Path("reports/metrics")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_coverage_report(
        self,
        endpoints: List[str],
        test_endpoint_mapping: Optional[Dict[str, List[str]]] = None
    ) -> CoverageMetrics:
        """
        Generate test coverage metrics for API endpoints.
        
        Args:
            endpoints: List of all available API endpoints
            test_endpoint_mapping: Mapping of test names to endpoints they cover
            
        Returns:
            CoverageMetrics with coverage data
        """
        if test_endpoint_mapping is None:
            test_endpoint_mapping = self._extract_endpoint_coverage()
        
        # Calculate coverage
        covered_endpoints = set()
        test_count_by_endpoint = {}
        
        for test_name, test_endpoints in test_endpoint_mapping.items():
            for endpoint in test_endpoints:
                covered_endpoints.add(endpoint)
                test_count_by_endpoint[endpoint] = test_count_by_endpoint.get(endpoint, 0) + 1
        
        total_endpoints = len(endpoints)
        covered_count = len(covered_endpoints)
        coverage_percentage = (covered_count / total_endpoints * 100) if total_endpoints > 0 else 0
        
        uncovered = [ep for ep in endpoints if ep not in covered_endpoints]
        
        coverage = CoverageMetrics(
            total_endpoints=total_endpoints,
            covered_endpoints=covered_count,
            coverage_percentage=round(coverage_percentage, 2),
            uncovered_endpoints=uncovered,
            test_count_by_endpoint=test_count_by_endpoint
        )
        
        # Save report
        self._save_json_report('coverage_metrics.json', asdict(coverage))
        
        return coverage
    
    def generate_trend_report(self, days: int = 30) -> TrendData:
        """
        Generate historical trend report.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            TrendData with historical trends
        """
        trends = self.collector.get_execution_trends(days=days)
        
        if not trends or 'trend_data' not in trends:
            return TrendData(
                period=f"Last {days} days",
                pass_rate_trend=[],
                duration_trend=[],
                test_count_trend=[],
                dates=[]
            )
        
        # Extract trend data
        trend_summaries = trends['trend_data']
        
        pass_rates = [s['pass_rate'] for s in trend_summaries]
        durations = [s['total_duration'] for s in trend_summaries]
        test_counts = [s['total_tests'] for s in trend_summaries]
        dates = [s['timestamp'][:10] for s in trend_summaries]  # Extract date only
        
        trend_data = TrendData(
            period=f"Last {days} days",
            pass_rate_trend=pass_rates,
            duration_trend=durations,
            test_count_trend=test_counts,
            dates=dates
        )
        
        # Save report
        self._save_json_report('trend_report.json', asdict(trend_data))
        
        return trend_data
    
    def generate_roi_report(
        self,
        manual_test_time_per_test: float = 5.0,  # minutes
        hourly_rate: float = 50.0,  # USD per hour
        days: int = 30
    ) -> ROIMetrics:
        """
        Generate ROI report for test automation.
        
        Args:
            manual_test_time_per_test: Average time for manual test execution (minutes)
            hourly_rate: Hourly rate for QA engineer (USD)
            days: Period to analyze
            
        Returns:
            ROIMetrics with ROI calculations
        """
        trends = self.collector.get_execution_trends(days=days)
        
        if not trends:
            return ROIMetrics(
                total_test_runs=0,
                total_time_saved_hours=0.0,
                manual_test_time_hours=0.0,
                automated_test_time_hours=0.0,
                time_savings_percentage=0.0,
                estimated_cost_savings=0.0,
                defects_found=0,
                defects_prevented=0
            )
        
        total_tests_executed = trends.get('total_tests_executed', 0)
        total_executions = trends.get('total_executions', 0)
        
        # Calculate time metrics
        manual_time_hours = (total_tests_executed * manual_test_time_per_test) / 60
        automated_time_hours = trends.get('average_duration', 0) * total_executions / 3600
        time_saved_hours = manual_time_hours - automated_time_hours
        time_savings_percentage = (time_saved_hours / manual_time_hours * 100) if manual_time_hours > 0 else 0
        
        # Calculate cost savings
        cost_savings = time_saved_hours * hourly_rate
        
        # Estimate defects (based on failed tests)
        defects_found = self._count_defects_found(days)
        defects_prevented = int(defects_found * 1.5)  # Estimate prevented defects
        
        roi = ROIMetrics(
            total_test_runs=total_executions,
            total_time_saved_hours=round(time_saved_hours, 2),
            manual_test_time_hours=round(manual_time_hours, 2),
            automated_test_time_hours=round(automated_time_hours, 2),
            time_savings_percentage=round(time_savings_percentage, 2),
            estimated_cost_savings=round(cost_savings, 2),
            defects_found=defects_found,
            defects_prevented=defects_prevented
        )
        
        # Save report
        self._save_json_report('roi_metrics.json', asdict(roi))
        
        return roi
    
    def generate_html_dashboard(self, days: int = 30) -> str:
        """
        Generate HTML dashboard with all metrics.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Path to generated HTML file
        """
        # Get all metrics
        trends = self.generate_trend_report(days=days)
        roi = self.generate_roi_report(days=days)
        flaky_tests = self.collector.get_flaky_tests()
        execution_trends = self.collector.get_execution_trends(days=days)
        
        # Generate HTML
        html_content = self._generate_html_content(
            trends=trends,
            roi=roi,
            flaky_tests=flaky_tests,
            execution_trends=execution_trends
        )
        
        # Save HTML file
        html_file = self.reports_dir / "quality_dashboard.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def generate_markdown_report(self, days: int = 30) -> str:
        """
        Generate markdown report with all metrics.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Path to generated markdown file
        """
        trends = self.generate_trend_report(days=days)
        roi = self.generate_roi_report(days=days)
        flaky_tests = self.collector.get_flaky_tests()
        execution_trends = self.collector.get_execution_trends(days=days)
        
        # Generate markdown content
        md_content = self._generate_markdown_content(
            trends=trends,
            roi=roi,
            flaky_tests=flaky_tests,
            execution_trends=execution_trends
        )
        
        # Save markdown file
        md_file = self.reports_dir / "quality_report.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return str(md_file)
    
    def _extract_endpoint_coverage(self) -> Dict[str, List[str]]:
        """Extract endpoint coverage from test names (heuristic)."""
        # This is a simplified implementation
        # In practice, you'd parse test code or use decorators
        return {}
    
    def _count_defects_found(self, days: int) -> int:
        """Count unique defects found in the period."""
        trends = self.collector.get_execution_trends(days=days)
        if not trends or 'trend_data' not in trends:
            return 0
        
        total_failures = sum(s.get('failed', 0) for s in trends['trend_data'])
        return total_failures
    
    def _save_json_report(self, filename: str, data: Dict):
        """Save report data as JSON."""
        filepath = self.reports_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def _generate_html_content(
        self,
        trends: TrendData,
        roi: ROIMetrics,
        flaky_tests: List,
        execution_trends: Dict
    ) -> str:
        """Generate HTML dashboard content with dark mode."""
        avg_pass_rate = execution_trends.get('average_pass_rate', 0)
        avg_duration = execution_trends.get('average_duration', 0)
        total_executions = execution_trends.get('total_executions', 0)
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Qualidade de Testes</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f7f5f2 0%, #ebe6df 50%, #f0ebe3 100%);
            color: #2d2a26;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: #ffffff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(204, 143, 101, 0.12);
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid rgba(204, 143, 101, 0.2);
        }}
        
        h1 {{
            color: #2d2a26;
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #c17d4a 0%, #d4915f 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .timestamp {{
            color: #6b5d52;
            font-size: 0.9em;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .timestamp::before {{
            content: "🕐";
        }}
        
        h2 {{
            color: #2d2a26;
            font-size: 1.8em;
            margin: 40px 0 20px 0;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin: 30px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #faf8f5 0%, #f5f1eb 100%);
            border: 1px solid rgba(204, 143, 101, 0.2);
            padding: 28px;
            border-radius: 16px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #c17d4a 0%, #d4915f 100%);
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(193, 125, 74, 0.15);
            border-color: rgba(204, 143, 101, 0.4);
        }}
        
        .metric-card.success {{
            background: linear-gradient(135deg, #f0f9f0 0%, #e8f5e9 100%);
            border-color: rgba(76, 175, 80, 0.25);
        }}
        
        .metric-card.success::before {{
            background: linear-gradient(90deg, #4caf50 0%, #66bb6a 100%);
        }}
        
        .metric-card.success:hover {{
            box-shadow: 0 8px 20px rgba(76, 175, 80, 0.15);
            border-color: rgba(76, 175, 80, 0.4);
        }}
        
        .metric-card.warning {{
            background: linear-gradient(135deg, #fff8f0 0%, #ffecdb 100%);
            border-color: rgba(255, 152, 0, 0.25);
        }}
        
        .metric-card.warning::before {{
            background: linear-gradient(90deg, #ff9800 0%, #ffa726 100%);
        }}
        
        .metric-card.warning:hover {{
            box-shadow: 0 8px 20px rgba(255, 152, 0, 0.15);
            border-color: rgba(255, 152, 0, 0.4);
        }}
        
        .metric-card.info {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
            border-color: rgba(100, 116, 139, 0.25);
        }}
        
        .metric-card.info::before {{
            background: linear-gradient(90deg, #64748b 0%, #94a3b8 100%);
        }}
        
        .metric-card.info:hover {{
            box-shadow: 0 8px 20px rgba(100, 116, 139, 0.15);
            border-color: rgba(100, 116, 139, 0.4);
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #6b5d52;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        
        .metric-value {{
            font-size: 3em;
            font-weight: 700;
            color: #2d2a26;
            line-height: 1;
        }}
        
        .flaky-tests {{
            background: linear-gradient(135deg, #fff8f0 0%, #ffecdb 100%);
            border: 1px solid rgba(255, 152, 0, 0.3);
            border-left: 4px solid #ff9800;
            padding: 24px;
            margin: 30px 0;
            border-radius: 12px;
        }}
        
        .flaky-tests h2 {{
            margin-top: 0;
            color: #e65100;
        }}
        
        .flaky-test-item {{
            margin: 16px 0;
            padding: 16px;
            background: #ffffff;
            border-radius: 8px;
            border-left: 3px solid #ff9800;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .flaky-test-item:hover {{
            background: #fafafa;
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
        }}
        
        .flaky-test-item strong {{
            color: #e65100;
            display: block;
            margin-bottom: 8px;
            font-size: 1.1em;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin: 30px 0;
            border-radius: 12px;
            background: #ffffff;
            border: 1px solid rgba(204, 143, 101, 0.15);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 16px;
            text-align: left;
            border-bottom: 1px solid rgba(204, 143, 101, 0.1);
        }}
        
        th {{
            background: linear-gradient(135deg, #faf8f5 0%, #f5f1eb 100%);
            color: #6b5d52;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
        }}
        
        tr:hover {{
            background: rgba(193, 125, 74, 0.03);
        }}
        
        td {{
            color: #4a4238;
        }}
        
        .no-data {{
            text-align: center;
            padding: 40px;
            color: #9e8b7b;
            font-style: italic;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge.success {{
            background: rgba(76, 175, 80, 0.15);
            color: #2e7d32;
        }}
        
        .badge.warning {{
            background: rgba(255, 152, 0, 0.15);
            color: #e65100;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
            
            .metric-value {{
                font-size: 2.5em;
            }}
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #f5f1eb;
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: rgba(193, 125, 74, 0.3);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(193, 125, 74, 0.5);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Dashboard de Qualidade de Testes</h1>
            <div class="timestamp">Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</div>
        </div>
        
        <h2>📊 Métricas Principais ({trends.period})</h2>
        <div class="metrics-grid">
            <div class="metric-card success">
                <div class="metric-label">Taxa de Sucesso Média</div>
                <div class="metric-value">{avg_pass_rate:.1f}%</div>
            </div>
            <div class="metric-card info">
                <div class="metric-label">Total de Execuções</div>
                <div class="metric-value">{total_executions}</div>
            </div>
            <div class="metric-card info">
                <div class="metric-label">Duração Média</div>
                <div class="metric-value">{avg_duration:.1f}s</div>
            </div>
            <div class="metric-card warning">
                <div class="metric-label">Testes Instáveis</div>
                <div class="metric-value">{len(flaky_tests)}</div>
            </div>
        </div>
        
        <h2>💰 Métricas de ROI</h2>
        <div class="metrics-grid">
            <div class="metric-card success">
                <div class="metric-label">Tempo Economizado</div>
                <div class="metric-value">{roi.total_time_saved_hours:.1f}h</div>
            </div>
            <div class="metric-card success">
                <div class="metric-label">Economia de Custos</div>
                <div class="metric-value">${roi.estimated_cost_savings:.0f}</div>
            </div>
            <div class="metric-card info">
                <div class="metric-label">% de Economia</div>
                <div class="metric-value">{roi.time_savings_percentage:.1f}%</div>
            </div>
            <div class="metric-card warning">
                <div class="metric-label">Defeitos Encontrados</div>
                <div class="metric-value">{roi.defects_found}</div>
            </div>
        </div>
        
        {self._generate_flaky_tests_html_dark(flaky_tests)}
        
        <h2>📈 Tendências de Execução</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Taxa de Sucesso</th>
                        <th>Duração (s)</th>
                        <th>Qtd. Testes</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_trend_table_rows(trends)}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_flaky_tests_html(self, flaky_tests: List) -> str:
        """Generate HTML section for flaky tests (legacy light mode)."""
        if not flaky_tests:
            return ""
        
        html = '<h2>⚠️ Flaky Tests Detected</h2><div class="flaky-tests">'
        for flaky in flaky_tests[:10]:  # Show top 10
            html += f"""
            <div class="flaky-test-item">
                <strong>{flaky.test_name}</strong><br>
                Flakiness Rate: {flaky.flakiness_rate * 100:.1f}% 
                ({flaky.failures}/{flaky.total_runs} failures)
            </div>
            """
        html += '</div>'
        return html
    
    def _generate_flaky_tests_html_dark(self, flaky_tests: List) -> str:
        """Generate HTML section for flaky tests (dark mode)."""
        if not flaky_tests:
            return """
            <div class="flaky-tests" style="background: linear-gradient(135deg, #f0f9f0 0%, #e8f5e9 100%); border-color: rgba(76, 175, 80, 0.3); border-left-color: #4caf50;">
                <h2 style="color: #2e7d32;">✅ Nenhum Teste Instável Detectado</h2>
                <p style="color: #388e3c; margin-top: 12px;">
                    Excelente! Todos os testes estão estáveis.
                </p>
            </div>
            """
        
        html = '<div class="flaky-tests"><h2>⚠️ Testes Instáveis Detectados</h2>'
        for flaky in flaky_tests[:10]:  # Show top 10
            html += f"""
            <div class="flaky-test-item">
                <strong>{flaky.test_name}</strong>
                <div style="color: #6b5d52; margin-top: 8px;">
                    Taxa de Instabilidade: <span style="color: #e65100;">{flaky.flakiness_rate * 100:.1f}%</span> 
                    ({flaky.failures}/{flaky.total_runs} falhas)
                </div>
            </div>
            """
        html += '</div>'
        return html
    
    def _generate_trend_table_rows(self, trends: TrendData) -> str:
        """Generate table rows for trend data."""
        rows = ""
        for i in range(min(10, len(trends.dates))):  # Show last 10
            rows += f"""
                <tr>
                    <td>{trends.dates[i]}</td>
                    <td>{trends.pass_rate_trend[i]:.1f}%</td>
                    <td>{trends.duration_trend[i]:.1f}</td>
                    <td>{trends.test_count_trend[i]}</td>
                </tr>
            """
        return rows
    
    def _generate_markdown_content(
        self,
        trends: TrendData,
        roi: ROIMetrics,
        flaky_tests: List,
        execution_trends: Dict
    ) -> str:
        """Generate markdown report content."""
        avg_pass_rate = execution_trends.get('average_pass_rate', 0)
        avg_duration = execution_trends.get('average_duration', 0)
        total_executions = execution_trends.get('total_executions', 0)
        
        md = f"""# Test Quality Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Executive Summary ({trends.period})

| Metric | Value |
|--------|-------|
| Average Pass Rate | {avg_pass_rate:.1f}% |
| Total Executions | {total_executions} |
| Average Duration | {avg_duration:.1f}s |
| Flaky Tests | {len(flaky_tests)} |

## 💰 ROI Metrics

| Metric | Value |
|--------|-------|
| Time Saved | {roi.total_time_saved_hours:.1f} hours |
| Cost Savings | ${roi.estimated_cost_savings:.2f} |
| Time Savings Percentage | {roi.time_savings_percentage:.1f}% |
| Defects Found | {roi.defects_found} |
| Defects Prevented (Est.) | {roi.defects_prevented} |

### ROI Details

- **Manual Test Time:** {roi.manual_test_time_hours:.1f} hours
- **Automated Test Time:** {roi.automated_test_time_hours:.1f} hours
- **Total Test Runs:** {roi.total_test_runs}

"""
        
        if flaky_tests:
            md += "\n## ⚠️ Flaky Tests\n\n"
            for flaky in flaky_tests[:10]:
                md += f"### {flaky.test_name}\n"
                md += f"- **Flakiness Rate:** {flaky.flakiness_rate * 100:.1f}%\n"
                md += f"- **Failures:** {flaky.failures}/{flaky.total_runs}\n"
                md += f"- **Last Failure:** {flaky.last_failure}\n\n"
        
        md += "\n## 📈 Execution Trends\n\n"
        md += "| Date | Pass Rate | Duration (s) | Test Count |\n"
        md += "|------|-----------|--------------|------------|\n"
        
        for i in range(min(10, len(trends.dates))):
            md += f"| {trends.dates[i]} | {trends.pass_rate_trend[i]:.1f}% | "
            md += f"{trends.duration_trend[i]:.1f} | {trends.test_count_trend[i]} |\n"
        
        return md


def generate_all_reports(days: int = 30) -> Dict[str, str]:
    """
    Generate all quality reports.
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Dictionary with paths to generated reports
    """
    reporter = MetricsReporter()
    
    html_path = reporter.generate_html_dashboard(days=days)
    md_path = reporter.generate_markdown_report(days=days)
    
    return {
        'html_dashboard': html_path,
        'markdown_report': md_path
    }
