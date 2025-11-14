"""
Allure Report Validation Script

This script validates that the Allure report contains all expected features:
- Dashboard statistics
- Test categorization by features and stories
- Severity levels
- Step descriptions
- Screenshot attachments
- Failure categories
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any


class AllureReportValidator:
    """Validates Allure report content and structure"""
    
    def __init__(self, results_dir: str = "reports/allure-results"):
        self.results_dir = Path(results_dir)
        self.validation_results = {
            "dashboard_statistics": False,
            "feature_categorization": False,
            "story_categorization": False,
            "severity_levels": False,
            "step_descriptions": False,
            "screenshot_attachments": False,
            "failure_categories": False
        }
        self.details = []
    
    def validate_all(self) -> bool:
        """Run all validation checks"""
        print("=" * 70)
        print("ALLURE REPORT VALIDATION")
        print("=" * 70)
        print()
        
        if not self.results_dir.exists():
            print(f"❌ ERROR: Results directory not found: {self.results_dir}")
            return False
        
        # Load all result files
        result_files = list(self.results_dir.glob("*-result.json"))
        container_files = list(self.results_dir.glob("*-container.json"))
        
        if not result_files:
            print("❌ ERROR: No test result files found")
            print(f"   Please run tests first: pytest tests/ --alluredir={self.results_dir}")
            return False
        
        print(f"📊 Found {len(result_files)} test results")
        print(f"📦 Found {len(container_files)} test containers")
        print()
        
        # Run validation checks
        self.validate_dashboard_statistics(result_files)
        self.validate_feature_categorization(result_files)
        self.validate_story_categorization(result_files)
        self.validate_severity_levels(result_files)
        self.validate_step_descriptions(result_files)
        self.validate_screenshot_attachments(result_files)
        self.validate_failure_categories()
        
        # Print results
        self.print_validation_summary()
        
        return all(self.validation_results.values())
    
    def validate_dashboard_statistics(self, result_files: List[Path]):
        """Verify dashboard can display statistics"""
        print("🔍 Validating Dashboard Statistics...")
        
        total_tests = len(result_files)
        statuses = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0}
        total_duration = 0
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    status = data.get("status", "unknown")
                    if status in statuses:
                        statuses[status] += 1
                    
                    start = data.get("start", 0)
                    stop = data.get("stop", 0)
                    if start and stop:
                        total_duration += (stop - start)
            except Exception as e:
                self.details.append(f"   ⚠️  Error reading {result_file.name}: {e}")
        
        if total_tests > 0:
            self.validation_results["dashboard_statistics"] = True
            self.details.append(f"   ✅ Total tests: {total_tests}")
            self.details.append(f"   ✅ Passed: {statuses['passed']}")
            self.details.append(f"   ✅ Failed: {statuses['failed']}")
            self.details.append(f"   ✅ Broken: {statuses['broken']}")
            self.details.append(f"   ✅ Skipped: {statuses['skipped']}")
            self.details.append(f"   ✅ Total duration: {total_duration / 1000:.2f}s")
        else:
            self.details.append("   ❌ No test statistics found")
        
        print()
    
    def validate_feature_categorization(self, result_files: List[Path]):
        """Check test categorization by features"""
        print("🔍 Validating Feature Categorization...")
        
        features = set()
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    labels = data.get("labels", [])
                    for label in labels:
                        if label.get("name") == "feature":
                            features.add(label.get("value"))
            except Exception as e:
                self.details.append(f"   ⚠️  Error reading {result_file.name}: {e}")
        
        if features:
            self.validation_results["feature_categorization"] = True
            self.details.append(f"   ✅ Found {len(features)} features:")
            for feature in sorted(features):
                self.details.append(f"      - {feature}")
        else:
            self.details.append("   ❌ No feature labels found")
            self.details.append("      Add @allure.feature() decorators to tests")
        
        print()
    
    def validate_story_categorization(self, result_files: List[Path]):
        """Check test categorization by stories"""
        print("🔍 Validating Story Categorization...")
        
        stories = set()
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    labels = data.get("labels", [])
                    for label in labels:
                        if label.get("name") == "story":
                            stories.add(label.get("value"))
            except Exception as e:
                self.details.append(f"   ⚠️  Error reading {result_file.name}: {e}")
        
        if stories:
            self.validation_results["story_categorization"] = True
            self.details.append(f"   ✅ Found {len(stories)} stories:")
            for story in sorted(stories):
                self.details.append(f"      - {story}")
        else:
            self.details.append("   ❌ No story labels found")
            self.details.append("      Add @allure.story() decorators to tests")
        
        print()
    
    def validate_severity_levels(self, result_files: List[Path]):
        """Confirm severity levels are present"""
        print("🔍 Validating Severity Levels...")
        
        severities = {}
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    labels = data.get("labels", [])
                    for label in labels:
                        if label.get("name") == "severity":
                            severity = label.get("value")
                            severities[severity] = severities.get(severity, 0) + 1
            except Exception as e:
                self.details.append(f"   ⚠️  Error reading {result_file.name}: {e}")
        
        if severities:
            self.validation_results["severity_levels"] = True
            self.details.append(f"   ✅ Found {len(severities)} severity levels:")
            for severity, count in sorted(severities.items()):
                self.details.append(f"      - {severity}: {count} tests")
        else:
            self.details.append("   ❌ No severity labels found")
            self.details.append("      Add @allure.severity() decorators to tests")
        
        print()
    
    def validate_step_descriptions(self, result_files: List[Path]):
        """Validate step descriptions appear correctly"""
        print("🔍 Validating Step Descriptions...")
        
        tests_with_steps = 0
        total_steps = 0
        step_examples = []
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    steps = data.get("steps", [])
                    if steps:
                        tests_with_steps += 1
                        total_steps += len(steps)
                        
                        # Collect first few step examples
                        if len(step_examples) < 3:
                            for step in steps[:2]:
                                step_name = step.get("name", "")
                                if step_name and step_name not in step_examples:
                                    step_examples.append(step_name)
            except Exception as e:
                self.details.append(f"   ⚠️  Error reading {result_file.name}: {e}")
        
        if tests_with_steps > 0:
            self.validation_results["step_descriptions"] = True
            self.details.append(f"   ✅ Found {tests_with_steps} tests with steps")
            self.details.append(f"   ✅ Total steps: {total_steps}")
            if step_examples:
                self.details.append("   ✅ Example steps:")
                for example in step_examples[:3]:
                    self.details.append(f"      - {example}")
        else:
            self.details.append("   ❌ No step descriptions found")
            self.details.append("      Add allure.step() to test implementations")
        
        print()
    
    def validate_screenshot_attachments(self, result_files: List[Path]):
        """Verify screenshots are attached to failed tests"""
        print("🔍 Validating Screenshot Attachments...")
        
        failed_tests = 0
        tests_with_screenshots = 0
        screenshot_files = []
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    status = data.get("status", "")
                    
                    if status in ["failed", "broken"]:
                        failed_tests += 1
                        attachments = data.get("attachments", [])
                        
                        for attachment in attachments:
                            if attachment.get("type") in ["image/png", "image/jpeg"]:
                                tests_with_screenshots += 1
                                screenshot_files.append(attachment.get("source", ""))
                                break
            except Exception as e:
                self.details.append(f"   ⚠️  Error reading {result_file.name}: {e}")
        
        if failed_tests == 0:
            self.validation_results["screenshot_attachments"] = True
            self.details.append("   ✅ No failed tests (screenshots not needed)")
        elif tests_with_screenshots > 0:
            self.validation_results["screenshot_attachments"] = True
            self.details.append(f"   ✅ Found {tests_with_screenshots}/{failed_tests} failed tests with screenshots")
            if screenshot_files:
                self.details.append(f"   ✅ Screenshot files: {len(screenshot_files)}")
        else:
            self.details.append(f"   ⚠️  Found {failed_tests} failed tests but no screenshots")
            self.details.append("      Screenshots may be added automatically on UI test failures")
        
        print()
    
    def validate_failure_categories(self):
        """Check failure categories are applied"""
        print("🔍 Validating Failure Categories...")
        
        categories_file = self.results_dir / "categories.json"
        
        if categories_file.exists():
            try:
                with open(categories_file, 'r', encoding='utf-8') as f:
                    categories = json.load(f)
                
                if categories and isinstance(categories, list):
                    self.validation_results["failure_categories"] = True
                    self.details.append(f"   ✅ Found {len(categories)} failure categories:")
                    for category in categories:
                        name = category.get("name", "Unknown")
                        self.details.append(f"      - {name}")
                else:
                    self.details.append("   ❌ categories.json is empty or invalid")
            except Exception as e:
                self.details.append(f"   ❌ Error reading categories.json: {e}")
        else:
            self.details.append("   ❌ categories.json not found")
            self.details.append(f"      Create file at: {categories_file}")
        
        print()
    
    def print_validation_summary(self):
        """Print validation summary"""
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print()
        
        for detail in self.details:
            print(detail)
        
        print()
        print("=" * 70)
        print("RESULTS")
        print("=" * 70)
        print()
        
        passed = sum(1 for v in self.validation_results.values() if v)
        total = len(self.validation_results)
        
        for check, result in self.validation_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {check.replace('_', ' ').title()}")
        
        print()
        print(f"Overall: {passed}/{total} checks passed")
        print()
        
        if passed == total:
            print("🎉 All validations passed! Allure report is properly configured.")
        else:
            print("⚠️  Some validations failed. Review the details above.")
        
        print("=" * 70)


def main():
    """Main entry point"""
    validator = AllureReportValidator()
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
