"""
Pytest plugin for automatic metrics collection.

This plugin hooks into pytest execution to automatically collect metrics
for all test runs without requiring manual instrumentation.
"""

import pytest
import time
from typing import Optional
from .metrics_collector import get_metrics_collector


class MetricsPlugin:
    """Pytest plugin for collecting test execution metrics."""
    
    def __init__(self):
        self.collector = get_metrics_collector()
        self.test_start_times = {}
    
    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionstart(self, session):
        """Called at the start of the test session."""
        self.collector.start_session()
    
    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        """Called before each test is executed."""
        self.test_start_times[item.nodeid] = time.time()
    
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Called after each test phase (setup, call, teardown)."""
        outcome = yield
        report = outcome.get_result()
        
        # Only process the 'call' phase (actual test execution)
        if report.when == 'call':
            test_name = item.nodeid
            start_time = self.test_start_times.get(test_name, time.time())
            duration = time.time() - start_time
            
            # Determine status
            if report.passed:
                status = 'passed'
            elif report.failed:
                status = 'failed'
            elif report.skipped:
                status = 'skipped'
            else:
                status = 'error'
            
            # Get error message if test failed
            error_message = None
            if report.failed and hasattr(report, 'longrepr'):
                error_message = str(report.longrepr)[:500]  # Limit to 500 chars
            
            # Extract markers
            markers = [marker.name for marker in item.iter_markers()]
            
            # Record the test
            self.collector.record_test(
                test_name=test_name,
                status=status,
                duration=duration,
                error_message=error_message,
                markers=markers
            )
    
    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        """Called at the end of the test session."""
        summary = self.collector.end_session()
        
        if summary:
            # Print summary to console
            print("\n" + "=" * 70)
            print("TEST EXECUTION METRICS SUMMARY")
            print("=" * 70)
            print(f"Total Tests: {summary.total_tests}")
            print(f"Passed: {summary.passed} ({summary.pass_rate}%)")
            print(f"Failed: {summary.failed} ({summary.fail_rate}%)")
            print(f"Skipped: {summary.skipped}")
            print(f"Errors: {summary.errors}")
            print(f"Total Duration: {summary.total_duration}s")
            print(f"Average Duration: {summary.average_duration}s")
            print("=" * 70)
            
            # Check for flaky tests
            flaky_tests = self.collector.get_flaky_tests()
            if flaky_tests:
                print("\nWARNING: FLAKY TESTS DETECTED:")
                for flaky in flaky_tests[:5]:  # Show top 5
                    print(f"  - {flaky.test_name}")
                    print(f"    Flakiness Rate: {flaky.flakiness_rate * 100}%")
                    print(f"    Failures: {flaky.failures}/{flaky.total_runs}")
                print("=" * 70)


def pytest_configure(config):
    """Register the metrics plugin with pytest."""
    if not config.option.collectonly:
        config.pluginmanager.register(MetricsPlugin(), "metrics_plugin")
