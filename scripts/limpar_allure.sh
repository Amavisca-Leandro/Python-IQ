#!/bin/bash
# ============================================================================
# Script: limpar_allure.sh
# Purpose: Clean old Allure results and reports
# Usage: ./limpar_allure.sh
# ============================================================================

echo ""
echo "========================================"
echo "  Allure Cleanup Utility"
echo "========================================"
echo ""

echo "This will delete:"
echo "  - All files in reports/allure-results/"
echo "  - All files in reports/allure-report/"
echo ""

# Prompt for confirmation
read -p "Are you sure you want to continue? (Y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo ""
    echo "[INFO] Cleanup cancelled."
    echo ""
    exit 0
fi

echo ""
echo "[INFO] Starting cleanup..."
echo ""

cleaned_results=0
cleaned_report=0

# Clean allure-results directory
if [ -d "reports/allure-results" ]; then
    echo "[INFO] Cleaning allure-results directory..."
    rm -rf reports/allure-results/*
    cleaned_results=1
    echo "[OK] Cleaned allure-results"
else
    echo "[INFO] Directory 'reports/allure-results' does not exist"
fi

echo ""

# Clean allure-report directory
if [ -d "reports/allure-report" ]; then
    echo "[INFO] Cleaning allure-report directory..."
    rm -rf reports/allure-report/*
    cleaned_report=1
    echo "[OK] Cleaned allure-report"
else
    echo "[INFO] Directory 'reports/allure-report' does not exist"
fi

echo ""
echo "========================================"
echo "  Cleanup Summary"
echo "========================================"
echo ""

if [ $cleaned_results -eq 1 ]; then
    echo "[✓] Allure results cleaned"
else
    echo "[−] No allure results to clean"
fi

if [ $cleaned_report -eq 1 ]; then
    echo "[✓] Allure report cleaned"
else
    echo "[−] No allure report to clean"
fi

echo ""
echo "[SUCCESS] Cleanup completed!"
echo ""
echo "You can now run tests to generate fresh results:"
echo "  pytest tests/ --alluredir=reports/allure-results"
echo ""
