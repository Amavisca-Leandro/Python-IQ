"""
Demo tests to showcase the metrics collection system.

These tests demonstrate how the metrics system automatically collects
execution data, detects flaky tests, and generates quality reports.
"""

import pytest
import time
import random


@pytest.mark.smoke
@pytest.mark.backend
def test_fast_passing_test():
    """A fast test that always passes."""
    time.sleep(0.1)
    assert True


@pytest.mark.regression
@pytest.mark.backend
def test_slow_passing_test():
    """A slower test that always passes."""
    time.sleep(0.5)
    assert 1 + 1 == 2


@pytest.mark.smoke
@pytest.mark.backend
def test_api_simulation():
    """Simulates an API test with some processing time."""
    time.sleep(0.2)
    result = {"status": "success", "data": [1, 2, 3]}
    assert result["status"] == "success"
    assert len(result["data"]) == 3


@pytest.mark.regression
def test_data_processing():
    """Simulates data processing test."""
    time.sleep(0.3)
    data = list(range(100))
    assert len(data) == 100
    assert sum(data) == 4950


@pytest.mark.slow
def test_integration_workflow():
    """Simulates a slow integration test."""
    time.sleep(1.0)
    # Simulate multi-step workflow
    step1 = True
    step2 = step1 and True
    step3 = step2 and True
    assert step3


# Uncomment to test flakiness detection
# @pytest.mark.backend
# def test_potentially_flaky():
#     """A test that fails randomly to demonstrate flakiness detection."""
#     # This will fail ~30% of the time
#     time.sleep(0.2)
#     assert random.random() > 0.3


@pytest.mark.skip(reason="Demonstrating skipped test metrics")
def test_skipped_test():
    """This test is skipped."""
    assert False


class TestMetricsCollection:
    """Test class to demonstrate metrics collection for test classes."""
    
    @pytest.mark.smoke
    def test_class_method_1(self):
        """First test in class."""
        time.sleep(0.1)
        assert True
    
    @pytest.mark.smoke
    def test_class_method_2(self):
        """Second test in class."""
        time.sleep(0.15)
        assert True
    
    @pytest.mark.regression
    def test_class_method_3(self):
        """Third test in class."""
        time.sleep(0.2)
        assert True


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_parametrized(value):
    """Parametrized test to show metrics for multiple test instances."""
    time.sleep(0.1)
    assert value > 0


def test_with_fixture(settings):
    """Test using a fixture to demonstrate fixture metrics."""
    time.sleep(0.1)
    assert settings is not None
    assert hasattr(settings, 'env')
