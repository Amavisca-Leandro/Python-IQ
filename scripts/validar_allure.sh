#!/bin/bash
# ============================================================================
# Allure Report Validation Script
# ============================================================================
# This script validates that the Allure report contains all expected features
# ============================================================================

echo ""
echo "============================================================================"
echo "ALLURE REPORT VALIDATION"
echo "============================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Run validation script
python3 scripts/validate_allure_report.py

if [ $? -eq 0 ]; then
    echo ""
    echo "[SUCCESS] Validation completed successfully!"
else
    echo ""
    echo "[WARNING] Some validation checks failed"
    echo "Review the output above for details"
fi

echo ""
