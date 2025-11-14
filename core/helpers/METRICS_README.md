# Test Metrics and Monitoring System

## Overview

The metrics and monitoring system provides comprehensive tracking and reporting of test execution metrics, including:

- **Execution Metrics**: Time, pass/fail rates, test counts
- **Flakiness Detection**: Automatic identification of unstable tests
- **Coverage Tracking**: API endpoint and feature coverage
- **Historical Trends**: Long-term quality and performance trends
- **ROI Calculations**: Cost savings and automation value

## Components

### 1. MetricsCollector (`metrics_collector.py`)

Collects and stores test execution metrics automatically.

**Features:**
- Records test execution time, status, and errors
- Tracks test history in JSONL format
- Detects flaky tests based on failure patterns
- Aggregates metrics by markers (smoke, regression, etc.)
- Generates execution summaries

**Usage:**
```python
from core.helpers.metrics_collector import get_metrics_collector

collector = get_metrics_collector()

# Start a test session
collector.start_session()

# Record a test
collector.record_test(
    test_name="test_user_login",
    status="passed",
    duration=1.5,
    markers=["smoke", "backend"]
)

# End session and get summary
summary = collector.end_session()
print(f"Pass Rate: {summary.pass_rate}%")

# Get flaky tests
flaky_tests = collector.get_flaky_tests()
for test in flaky_tests:
    print(f"{test.test_name}: {test.flakiness_rate * 100}% flaky")
```

### 2. Pytest Plugin (`pytest_metrics_plugin.py`)

Automatically collects metrics during pytest execution.

**Features:**
- Hooks into pytest lifecycle
- No manual instrumentation required
- Displays summary after test run
- Warns about flaky tests

**Activation:**
The plugin is automatically activated when pytest runs. It's registered in `tests/conftest.py`:

```python
pytest_plugins = [
    "core.helpers.pytest_metrics_plugin"
]
```

**Output Example:**
```
======================================================================
TEST EXECUTION METRICS SUMMARY
======================================================================
Total Tests: 45
Passed: 42 (93.33%)
Failed: 3 (6.67%)
Skipped: 0
Errors: 0
Total Duration: 125.5s
Average Duration: 2.79s
======================================================================

⚠️  FLAKY TESTS DETECTED:
  - tests/backend/test_api.py::test_user_creation
    Flakiness Rate: 25.0%
    Failures: 5/20
======================================================================
```

### 3. MetricsReporter (`metrics_reporter.py`)

Generates comprehensive quality reports and dashboards.

**Features:**
- HTML dashboards with visualizations
- Markdown reports for documentation
- Coverage metrics calculation
- ROI analysis
- Historical trend analysis

**Usage:**
```python
from core.helpers.metrics_reporter import MetricsReporter

reporter = MetricsReporter()

# Generate HTML dashboard
html_path = reporter.generate_html_dashboard(days=30)
print(f"Dashboard: {html_path}")

# Generate markdown report
md_path = reporter.generate_markdown_report(days=30)

# Get ROI metrics
roi = reporter.generate_roi_report(
    manual_test_time_per_test=5.0,  # minutes
    hourly_rate=50.0,  # USD
    days=30
)
print(f"Time Saved: {roi.total_time_saved_hours} hours")
print(f"Cost Savings: ${roi.estimated_cost_savings}")

# Get trend data
trends = reporter.generate_trend_report(days=30)
print(f"Average Pass Rate: {trends.pass_rate_trend}")
```

## Data Storage

Metrics are stored in `reports/metrics/`:

```
reports/metrics/
├── test_metrics.jsonl          # Raw test execution data (JSONL format)
├── execution_summary.json      # Aggregated execution summaries
├── flaky_tests.json           # Detected flaky tests
├── coverage_metrics.json      # Coverage data
├── trend_report.json          # Historical trends
├── roi_metrics.json           # ROI calculations
├── quality_dashboard.html     # HTML dashboard
└── quality_report.md          # Markdown report
```

### Data Format

**test_metrics.jsonl** (one JSON object per line):
```json
{"test_id": "test_login_1234567890", "test_name": "tests/backend/test_auth.py::test_login", "status": "passed", "duration": 1.5, "timestamp": "2024-01-15T10:30:00", "error_message": null, "markers": ["smoke", "backend"]}
```

**execution_summary.json**:
```json
[
  {
    "total_tests": 45,
    "passed": 42,
    "failed": 3,
    "skipped": 0,
    "errors": 0,
    "total_duration": 125.5,
    "pass_rate": 93.33,
    "fail_rate": 6.67,
    "average_duration": 2.79,
    "timestamp": "2024-01-15T10:35:00"
  }
]
```

## Generating Reports

### Using Python Script

```bash
# Generate all reports for last 30 days
python scripts/generate_metrics_report.py --days 30 --format all

# Generate only HTML dashboard
python scripts/generate_metrics_report.py --days 7 --format html

# Show flaky tests and trends
python scripts/generate_metrics_report.py --days 30 --show-flaky --show-trends
```

### Using Batch Script (Windows)

```cmd
# Generate reports with default settings (30 days, all formats)
scripts\gerar_relatorio_metricas.bat

# Generate reports for last 7 days
scripts\gerar_relatorio_metricas.bat 7 html

# Generate markdown report for last 14 days
scripts\gerar_relatorio_metricas.bat 14 markdown
```

## Flakiness Detection

The system automatically detects flaky tests using the following criteria:

- **Minimum Runs**: Test must have run at least 5 times
- **Flakiness Threshold**: Failure rate between 20% and 80%
- **Detection Logic**: Tests that sometimes pass and sometimes fail

**Example:**
```python
from core.helpers.metrics_collector import get_metrics_collector

collector = get_metrics_collector()
flaky_tests = collector.get_flaky_tests(
    min_runs=5,
    flakiness_threshold=0.2
)

for test in flaky_tests:
    print(f"Test: {test.test_name}")
    print(f"Flakiness: {test.flakiness_rate * 100}%")
    print(f"Runs: {test.total_runs}, Failures: {test.failures}")
    print(f"Last Failure: {test.last_failure}")
    print(f"Recent Errors: {test.failure_messages[-3:]}")
```

## ROI Calculation

The system calculates Return on Investment for test automation:

**Formula:**
```
Manual Time = Total Tests × Manual Test Time per Test
Automated Time = Average Duration × Total Executions
Time Saved = Manual Time - Automated Time
Cost Savings = Time Saved × Hourly Rate
```

**Example:**
```python
roi = reporter.generate_roi_report(
    manual_test_time_per_test=5.0,  # 5 minutes per test manually
    hourly_rate=50.0,                # $50/hour QA engineer rate
    days=30                          # Last 30 days
)

print(f"Manual Time: {roi.manual_test_time_hours}h")
print(f"Automated Time: {roi.automated_test_time_hours}h")
print(f"Time Saved: {roi.total_time_saved_hours}h ({roi.time_savings_percentage}%)")
print(f"Cost Savings: ${roi.estimated_cost_savings}")
print(f"Defects Found: {roi.defects_found}")
```

## Integration with CI/CD

The metrics system integrates seamlessly with CI/CD pipelines:

### GitHub Actions Example

```yaml
- name: Run Tests with Metrics
  run: |
    pytest --alluredir=reports/allure-results
    
- name: Generate Metrics Report
  run: |
    python scripts/generate_metrics_report.py --days 30 --format all
    
- name: Upload Metrics Reports
  uses: actions/upload-artifact@v3
  with:
    name: metrics-reports
    path: reports/metrics/
```

## Best Practices

1. **Regular Monitoring**: Generate reports weekly to track trends
2. **Address Flaky Tests**: Prioritize fixing tests with >30% flakiness
3. **Track Coverage**: Monitor endpoint coverage to identify gaps
4. **Review ROI**: Use ROI metrics to justify automation investments
5. **Historical Analysis**: Keep at least 90 days of metrics data

## Troubleshooting

### No Metrics Data

**Problem**: Reports show no data

**Solution**:
- Ensure tests have been run with the metrics plugin enabled
- Check that `reports/metrics/test_metrics.jsonl` exists
- Verify pytest is using the correct conftest.py

### Flaky Tests Not Detected

**Problem**: Known flaky tests not appearing in reports

**Solution**:
- Ensure test has run at least 5 times (configurable)
- Check flakiness threshold (default 20%)
- Verify test names are consistent across runs

### Performance Impact

**Problem**: Metrics collection slowing down tests

**Solution**:
- Metrics collection has minimal overhead (<1%)
- Disable in production: `pytest --no-metrics` (if configured)
- Use session-scoped collectors for better performance

## API Reference

### MetricsCollector

```python
class MetricsCollector:
    def start_session() -> None
    def record_test(test_name, status, duration, error_message, markers) -> None
    def end_session() -> TestExecutionSummary
    def get_test_history(test_name, limit=10) -> List[TestMetric]
    def get_flaky_tests(min_runs=5, flakiness_threshold=0.2) -> List[FlakyTest]
    def get_metrics_by_marker(marker) -> Dict[str, Any]
    def get_execution_trends(days=7) -> Dict[str, Any]
```

### MetricsReporter

```python
class MetricsReporter:
    def generate_coverage_report(endpoints, test_endpoint_mapping) -> CoverageMetrics
    def generate_trend_report(days=30) -> TrendData
    def generate_roi_report(manual_test_time_per_test, hourly_rate, days) -> ROIMetrics
    def generate_html_dashboard(days=30) -> str
    def generate_markdown_report(days=30) -> str
```

## Examples

### Example 1: Daily Metrics Check

```python
from core.helpers.metrics_collector import get_metrics_collector

collector = get_metrics_collector()

# Get yesterday's metrics
trends = collector.get_execution_trends(days=1)
print(f"Pass Rate: {trends['average_pass_rate']}%")

# Check for new flaky tests
flaky = collector.get_flaky_tests()
if flaky:
    print(f"⚠️  {len(flaky)} flaky tests detected!")
```

### Example 2: Weekly Report Generation

```python
from core.helpers.metrics_reporter import generate_all_reports

# Generate all reports for the week
reports = generate_all_reports(days=7)
print(f"HTML Dashboard: {reports['html_dashboard']}")
print(f"Markdown Report: {reports['markdown_report']}")
```

### Example 3: Custom Metrics Analysis

```python
from core.helpers.metrics_collector import get_metrics_collector

collector = get_metrics_collector()

# Get metrics for smoke tests only
smoke_metrics = collector.get_metrics_by_marker('smoke')
print(f"Smoke Tests Pass Rate: {smoke_metrics['pass_rate']}%")

# Get metrics for backend tests
backend_metrics = collector.get_metrics_by_marker('backend')
print(f"Backend Tests Average Duration: {backend_metrics['average_duration']}s")
```

## Future Enhancements

- Real-time dashboard with auto-refresh
- Integration with Grafana/Prometheus
- Slack/Email notifications for quality degradation
- Machine learning for flakiness prediction
- Test execution cost optimization recommendations
