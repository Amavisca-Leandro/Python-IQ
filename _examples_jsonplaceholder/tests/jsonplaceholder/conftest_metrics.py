"""
Pytest plugin for collecting JSONPlaceholder API test metrics.

This module provides hooks to collect and report:
- Endpoint coverage metrics
- Performance metrics
- Success rates by resource and operation
"""

import pytest
import time
from collections import defaultdict
from typing import Dict, List, Any


class APIMetricsCollector:
    """Collects metrics during test execution."""
    
    def __init__(self):
        self.endpoint_calls: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.test_results: Dict[str, str] = {}
        self.performance_data: List[Dict[str, Any]] = []
        
    def record_api_call(self, endpoint: str, method: str, status_code: int, 
                       response_time_ms: float, test_name: str):
        """Record an API call for metrics."""
        self.endpoint_calls[f"{method} {endpoint}"].append({
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "test_name": test_name
        })
        
        self.performance_data.append({
            "endpoint": endpoint,
            "method": method,
            "response_time_ms": response_time_ms,
            "test_name": test_name
        })
    
    def record_test_result(self, test_name: str, outcome: str):
        """Record test result (passed/failed/skipped)."""
        self.test_results[test_name] = outcome
    
    def get_endpoint_coverage(self) -> Dict[str, int]:
        """Get count of tests per endpoint."""
        coverage = defaultdict(int)
        for endpoint in self.endpoint_calls.keys():
            coverage[endpoint] = len(self.endpoint_calls[endpoint])
        return dict(coverage)
    
    def get_success_rate_by_resource(self) -> Dict[str, Dict[str, Any]]:
        """Calculate success rate by resource (posts, users, etc.)."""
        resources = ["posts", "users", "comments", "todos", "albums"]
        stats = {}
        
        for resource in resources:
            resource_tests = [
                (name, outcome) for name, outcome in self.test_results.items()
                if resource in name
            ]
            
            if resource_tests:
                total = len(resource_tests)
                passed = sum(1 for _, outcome in resource_tests if outcome == "passed")
                stats[resource] = {
                    "total": total,
                    "passed": passed,
                    "failed": total - passed,
                    "success_rate": (passed / total * 100) if total > 0 else 0
                }
        
        return stats
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics."""
        if not self.performance_data:
            return {}
        
        response_times = [d["response_time_ms"] for d in self.performance_data]
        
        # Group by endpoint
        endpoint_times = defaultdict(list)
        for data in self.performance_data:
            key = f"{data['method']} {data['endpoint']}"
            endpoint_times[key].append(data["response_time_ms"])
        
        # Find slowest endpoint
        slowest_endpoint = None
        slowest_time = 0
        for endpoint, times in endpoint_times.items():
            avg_time = sum(times) / len(times)
            if avg_time > slowest_time:
                slowest_time = avg_time
                slowest_endpoint = endpoint
        
        # Count threshold violations (>1000ms)
        violations = sum(1 for t in response_times if t > 1000)
        
        return {
            "average_response_time_ms": sum(response_times) / len(response_times),
            "min_response_time_ms": min(response_times),
            "max_response_time_ms": max(response_times),
            "slowest_endpoint": slowest_endpoint,
            "slowest_endpoint_time_ms": slowest_time,
            "threshold_violations": violations,
            "total_requests": len(response_times)
        }
    
    def generate_report(self) -> str:
        """Generate a formatted metrics report."""
        lines = []
        lines.append("\n" + "="*70)
        lines.append("JSONPlaceholder API Test Metrics Report")
        lines.append("="*70)
        
        # Summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for outcome in self.test_results.values() if outcome == "passed")
        failed_tests = total_tests - passed_tests
        
        lines.append("\nSummary:")
        lines.append(f"  Total Tests: {total_tests}")
        lines.append(f"  Passed: {passed_tests}")
        lines.append(f"  Failed: {failed_tests}")
        lines.append(f"  Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "  Success Rate: N/A")
        
        # Endpoint Coverage
        lines.append("\nEndpoint Coverage:")
        coverage = self.get_endpoint_coverage()
        for endpoint, count in sorted(coverage.items()):
            lines.append(f"  {endpoint}: {count} tests")
        
        # Success Rate by Resource
        lines.append("\nSuccess Rate by Resource:")
        resource_stats = self.get_success_rate_by_resource()
        for resource, stats in sorted(resource_stats.items()):
            lines.append(
                f"  /{resource}: {stats['passed']}/{stats['total']} tests "
                f"({stats['success_rate']:.1f}%)"
            )
        
        # Performance Metrics
        perf_summary = self.get_performance_summary()
        if perf_summary:
            lines.append("\nPerformance Metrics:")
            lines.append(f"  Total API Calls: {perf_summary['total_requests']}")
            lines.append(f"  Average Response Time: {perf_summary['average_response_time_ms']:.2f}ms")
            lines.append(f"  Min Response Time: {perf_summary['min_response_time_ms']:.2f}ms")
            lines.append(f"  Max Response Time: {perf_summary['max_response_time_ms']:.2f}ms")
            if perf_summary['slowest_endpoint']:
                lines.append(f"  Slowest Endpoint: {perf_summary['slowest_endpoint']} "
                           f"({perf_summary['slowest_endpoint_time_ms']:.2f}ms)")
            lines.append(f"  Threshold Violations (>1000ms): {perf_summary['threshold_violations']}")
        
        lines.append("\n" + "="*70 + "\n")
        
        return "\n".join(lines)


# Global metrics collector instance
_metrics_collector = None


def get_metrics_collector():
    """Get or create the global metrics collector."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = APIMetricsCollector()
    return _metrics_collector


# Pytest hooks

def pytest_configure(config):
    """Initialize metrics collector at start of test session."""
    global _metrics_collector
    _metrics_collector = APIMetricsCollector()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        collector = get_metrics_collector()
        test_name = item.nodeid
        
        if report.passed:
            collector.record_test_result(test_name, "passed")
        elif report.failed:
            collector.record_test_result(test_name, "failed")
        elif report.skipped:
            collector.record_test_result(test_name, "skipped")


def pytest_sessionfinish(session, exitstatus):
    """Generate and print metrics report at end of test session."""
    collector = get_metrics_collector()
    
    # Print report to console
    report = collector.generate_report()
    print(report)
    
    # Save report to file
    try:
        with open("reports/jsonplaceholder_metrics.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Metrics report saved to: reports/jsonplaceholder_metrics.txt")
    except Exception as e:
        print(f"Warning: Could not save metrics report: {e}")


# Fixture to track API calls in tests
@pytest.fixture
def track_api_metrics(request):
    """
    Fixture to automatically track API metrics for tests.
    
    Usage in tests:
        def test_something(jsonplaceholder_client, track_api_metrics):
            response = jsonplaceholder_client.get_posts()
            track_api_metrics(response, "GET", "/posts")
    """
    collector = get_metrics_collector()
    test_name = request.node.nodeid
    
    def track(response, method: str, endpoint: str):
        """Track an API call."""
        response_time_ms = response.elapsed.total_seconds() * 1000
        collector.record_api_call(
            endpoint=endpoint,
            method=method,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            test_name=test_name
        )
    
    return track
