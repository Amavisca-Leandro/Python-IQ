"""
Simple test to verify Test Explorer can discover BDD tests.

This is a basic pytest test (not pytest-bdd) to ensure the directory
is being scanned by the Test Explorer.
"""

import pytest


def test_bdd_directory_is_discoverable():
    """
    Simple test to verify Test Explorer discovers tests in bdd directory.
    
    If you can see this test in Test Explorer, it means the bdd directory
    is being scanned correctly.
    """
    assert True, "BDD directory is discoverable!"


def test_pytest_is_working():
    """Verify pytest is working correctly in bdd directory."""
    assert 1 + 1 == 2


def test_bdd_tests_count():
    """Verify we have the expected number of BDD test files."""
    import os
    from pathlib import Path
    
    bdd_dir = Path(__file__).parent
    test_files = list(bdd_dir.glob("test_*.py"))
    
    # Should have at least 7 test files
    assert len(test_files) >= 7, f"Expected at least 7 test files, found {len(test_files)}"


@pytest.mark.smoke
def test_bdd_smoke_marker():
    """Test that markers work in BDD directory."""
    assert True


class TestBDDDiscovery:
    """Test class to verify class-based tests are discovered."""
    
    def test_class_based_test(self):
        """Verify class-based tests work in BDD directory."""
        assert True
    
    def test_another_class_test(self):
        """Another test in the class."""
        assert 2 + 2 == 4
