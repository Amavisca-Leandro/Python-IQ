"""
Metrics Collector for Test Execution Monitoring.

This module provides functionality to collect and track test execution metrics including:
- Execution time per test
- Success/failure rates
- Flakiness detection
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class TestMetric:
    """Represents metrics for a single test execution."""
    test_id: str
    test_name: str
    status: str  # passed, failed, skipped, error
    duration: float  # in seconds
    timestamp: str
    error_message: Optional[str] = None
    markers: List[str] = None
    
    def __post_init__(self):
        if self.markers is None:
            self.markers = []


@dataclass
class TestExecutionSummary:
    """Summary of test execution metrics."""
    total_tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    total_duration: float
    pass_rate: float
    fail_rate: float
    average_duration: float
    timestamp: str


@dataclass
class FlakyTest:
    """Represents a flaky test with its failure history."""
    test_name: str
    total_runs: int
    failures: int
    flakiness_rate: float
    last_failure: str
    failure_messages: List[str]


class MetricsCollector:
    """Collects and manages test execution metrics."""
    
    def __init__(self, metrics_dir: str = "reports/metrics"):
        """
        Initialize the metrics collector.
        
        Args:
            metrics_dir: Directory to store metrics data
        """
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session_metrics: List[TestMetric] = []
        self.session_start_time: Optional[float] = None
        
        # Files for persistent storage
        self.metrics_file = self.metrics_dir / "test_metrics.jsonl"
        self.summary_file = self.metrics_dir / "execution_summary.json"
        self.flaky_tests_file = self.metrics_dir / "flaky_tests.json"
    
    def start_session(self):
        """Mark the start of a test session."""
        self.session_start_time = time.time()
        self.current_session_metrics = []
    
    def record_test(
        self,
        test_name: str,
        status: str,
        duration: float,
        error_message: Optional[str] = None,
        markers: Optional[List[str]] = None
    ):
        """
        Record metrics for a single test execution.
        
        Args:
            test_name: Full test name (module::class::method)
            status: Test status (passed, failed, skipped, error)
            duration: Test execution time in seconds
            error_message: Error message if test failed
            markers: List of pytest markers applied to the test
        """
        test_id = f"{test_name}_{int(time.time() * 1000)}"
        timestamp = datetime.now().isoformat()
        
        metric = TestMetric(
            test_id=test_id,
            test_name=test_name,
            status=status,
            duration=duration,
            timestamp=timestamp,
            error_message=error_message,
            markers=markers or []
        )
        
        self.current_session_metrics.append(metric)
        self._append_to_metrics_file(metric)
    
    def end_session(self) -> TestExecutionSummary:
        """
        End the test session and generate summary.
        
        Returns:
            TestExecutionSummary with aggregated metrics
        """
        if not self.current_session_metrics:
            return None
        
        total_tests = len(self.current_session_metrics)
        passed = sum(1 for m in self.current_session_metrics if m.status == "passed")
        failed = sum(1 for m in self.current_session_metrics if m.status == "failed")
        skipped = sum(1 for m in self.current_session_metrics if m.status == "skipped")
        errors = sum(1 for m in self.current_session_metrics if m.status == "error")
        
        total_duration = sum(m.duration for m in self.current_session_metrics)
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        fail_rate = (failed / total_tests * 100) if total_tests > 0 else 0
        average_duration = total_duration / total_tests if total_tests > 0 else 0
        
        summary = TestExecutionSummary(
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            total_duration=round(total_duration, 2),
            pass_rate=round(pass_rate, 2),
            fail_rate=round(fail_rate, 2),
            average_duration=round(average_duration, 2),
            timestamp=datetime.now().isoformat()
        )
        
        self._save_summary(summary)
        self._detect_flaky_tests()
        
        return summary
    
    def get_test_history(self, test_name: str, limit: int = 10) -> List[TestMetric]:
        """
        Get execution history for a specific test.
        
        Args:
            test_name: Name of the test
            limit: Maximum number of records to return
            
        Returns:
            List of TestMetric objects for the test
        """
        if not self.metrics_file.exists():
            return []
        
        history = []
        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                metric_data = json.loads(line)
                if metric_data['test_name'] == test_name:
                    history.append(TestMetric(**metric_data))
                    if len(history) >= limit:
                        break
        
        return history
    
    def get_flaky_tests(self, min_runs: int = 5, flakiness_threshold: float = 0.2) -> List[FlakyTest]:
        """
        Identify flaky tests based on historical data.
        
        Args:
            min_runs: Minimum number of runs to consider a test
            flakiness_threshold: Minimum failure rate to consider flaky (0.0-1.0)
            
        Returns:
            List of FlakyTest objects
        """
        if not self.metrics_file.exists():
            return []
        
        # Aggregate test results
        test_results: Dict[str, List[TestMetric]] = defaultdict(list)
        
        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                metric_data = json.loads(line)
                metric = TestMetric(**metric_data)
                test_results[metric.test_name].append(metric)
        
        # Identify flaky tests
        flaky_tests = []
        for test_name, metrics in test_results.items():
            if len(metrics) < min_runs:
                continue
            
            failures = [m for m in metrics if m.status in ('failed', 'error')]
            failure_count = len(failures)
            total_runs = len(metrics)
            flakiness_rate = failure_count / total_runs
            
            if 0 < flakiness_rate < 1.0 and flakiness_rate >= flakiness_threshold:
                last_failure = failures[-1].timestamp if failures else None
                failure_messages = [f.error_message for f in failures if f.error_message]
                
                flaky_test = FlakyTest(
                    test_name=test_name,
                    total_runs=total_runs,
                    failures=failure_count,
                    flakiness_rate=round(flakiness_rate, 2),
                    last_failure=last_failure,
                    failure_messages=failure_messages[-5:]  # Last 5 failure messages
                )
                flaky_tests.append(flaky_test)
        
        # Sort by flakiness rate
        flaky_tests.sort(key=lambda x: x.flakiness_rate, reverse=True)
        
        return flaky_tests
    
    def get_metrics_by_marker(self, marker: str) -> Dict[str, Any]:
        """
        Get aggregated metrics for tests with a specific marker.
        
        Args:
            marker: Pytest marker name (e.g., 'smoke', 'regression')
            
        Returns:
            Dictionary with aggregated metrics
        """
        if not self.metrics_file.exists():
            return {}
        
        matching_metrics = []
        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                metric_data = json.loads(line)
                if marker in metric_data.get('markers', []):
                    matching_metrics.append(TestMetric(**metric_data))
        
        if not matching_metrics:
            return {}
        
        total = len(matching_metrics)
        passed = sum(1 for m in matching_metrics if m.status == "passed")
        failed = sum(1 for m in matching_metrics if m.status == "failed")
        
        return {
            'marker': marker,
            'total_tests': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': round(passed / total * 100, 2) if total > 0 else 0,
            'average_duration': round(
                sum(m.duration for m in matching_metrics) / total, 2
            ) if total > 0 else 0
        }
    
    def _append_to_metrics_file(self, metric: TestMetric):
        """Append a metric to the JSONL metrics file."""
        with open(self.metrics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(metric)) + '\n')
    
    def _save_summary(self, summary: TestExecutionSummary):
        """Save execution summary to JSON file."""
        # Load existing summaries
        summaries = []
        if self.summary_file.exists():
            with open(self.summary_file, 'r', encoding='utf-8') as f:
                summaries = json.load(f)
        
        # Append new summary
        summaries.append(asdict(summary))
        
        # Keep only last 100 summaries
        summaries = summaries[-100:]
        
        # Save back
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2)
    
    def _detect_flaky_tests(self):
        """Detect and save flaky tests."""
        flaky_tests = self.get_flaky_tests()
        
        if flaky_tests:
            flaky_data = [asdict(ft) for ft in flaky_tests]
            with open(self.flaky_tests_file, 'w', encoding='utf-8') as f:
                json.dump(flaky_data, f, indent=2)
    
    def get_execution_trends(self, days: int = 7) -> Dict[str, Any]:
        """
        Get execution trends over the specified number of days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend data
        """
        if not self.summary_file.exists():
            return {}
        
        with open(self.summary_file, 'r', encoding='utf-8') as f:
            summaries = json.load(f)
        
        if not summaries:
            return {}
        
        # Filter summaries by date range
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        recent_summaries = [
            s for s in summaries
            if datetime.fromisoformat(s['timestamp']).timestamp() > cutoff_date
        ]
        
        if not recent_summaries:
            return {}
        
        return {
            'period_days': days,
            'total_executions': len(recent_summaries),
            'average_pass_rate': round(
                sum(s['pass_rate'] for s in recent_summaries) / len(recent_summaries), 2
            ),
            'average_duration': round(
                sum(s['total_duration'] for s in recent_summaries) / len(recent_summaries), 2
            ),
            'total_tests_executed': sum(s['total_tests'] for s in recent_summaries),
            'trend_data': recent_summaries
        }


# Global instance for easy access
_metrics_collector = None


def get_metrics_collector(metrics_dir: str = "reports/metrics") -> MetricsCollector:
    """
    Get or create the global metrics collector instance.
    
    Args:
        metrics_dir: Directory to store metrics data
        
    Returns:
        MetricsCollector instance
    """
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector(metrics_dir)
    return _metrics_collector
