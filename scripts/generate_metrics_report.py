"""
Script to generate test metrics and quality reports.

Usage:
    python scripts/generate_metrics_report.py [--days DAYS] [--format FORMAT]

Examples:
    python scripts/generate_metrics_report.py --days 30 --format html
    python scripts/generate_metrics_report.py --days 7 --format markdown
    python scripts/generate_metrics_report.py --days 30 --format all
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.helpers.metrics_reporter import MetricsReporter, generate_all_reports
from core.helpers.metrics_collector import get_metrics_collector


def main():
    """Main entry point for metrics report generation."""
    parser = argparse.ArgumentParser(
        description='Generate test metrics and quality reports'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to analyze (default: 30)'
    )
    parser.add_argument(
        '--format',
        choices=['html', 'markdown', 'all'],
        default='all',
        help='Report format (default: all)'
    )
    parser.add_argument(
        '--show-flaky',
        action='store_true',
        help='Show flaky tests in console'
    )
    parser.add_argument(
        '--show-trends',
        action='store_true',
        help='Show execution trends in console'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("GENERATING TEST METRICS REPORTS")
    print("=" * 70)
    print(f"Analysis Period: Last {args.days} days")
    print(f"Report Format: {args.format}")
    print()
    
    # Initialize reporter
    reporter = MetricsReporter()
    collector = get_metrics_collector()
    
    # Generate reports based on format
    generated_files = []
    
    if args.format in ('html', 'all'):
        print("Generating HTML dashboard...")
        html_path = reporter.generate_html_dashboard(days=args.days)
        generated_files.append(html_path)
        print(f"✓ HTML dashboard: {html_path}")
    
    if args.format in ('markdown', 'all'):
        print("Generating Markdown report...")
        md_path = reporter.generate_markdown_report(days=args.days)
        generated_files.append(md_path)
        print(f"✓ Markdown report: {md_path}")
    
    # Generate additional reports
    print("\nGenerating additional metrics...")
    
    trends = reporter.generate_trend_report(days=args.days)
    print(f"✓ Trend report generated")
    
    roi = reporter.generate_roi_report(days=args.days)
    print(f"✓ ROI metrics calculated")
    
    # Show flaky tests if requested
    if args.show_flaky:
        print("\n" + "=" * 70)
        print("FLAKY TESTS DETECTED")
        print("=" * 70)
        
        flaky_tests = collector.get_flaky_tests()
        if flaky_tests:
            for i, flaky in enumerate(flaky_tests[:10], 1):
                print(f"\n{i}. {flaky.test_name}")
                print(f"   Flakiness Rate: {flaky.flakiness_rate * 100:.1f}%")
                print(f"   Failures: {flaky.failures}/{flaky.total_runs}")
                print(f"   Last Failure: {flaky.last_failure}")
        else:
            print("No flaky tests detected! 🎉")
    
    # Show trends if requested
    if args.show_trends:
        print("\n" + "=" * 70)
        print("EXECUTION TRENDS")
        print("=" * 70)
        
        execution_trends = collector.get_execution_trends(days=args.days)
        if execution_trends:
            print(f"\nPeriod: Last {args.days} days")
            print(f"Total Executions: {execution_trends.get('total_executions', 0)}")
            print(f"Average Pass Rate: {execution_trends.get('average_pass_rate', 0):.1f}%")
            print(f"Average Duration: {execution_trends.get('average_duration', 0):.1f}s")
            print(f"Total Tests Executed: {execution_trends.get('total_tests_executed', 0)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Reports generated: {len(generated_files)}")
    for file_path in generated_files:
        print(f"  - {file_path}")
    
    print("\n✓ Metrics report generation completed successfully!")
    print("=" * 70)


if __name__ == '__main__':
    main()
