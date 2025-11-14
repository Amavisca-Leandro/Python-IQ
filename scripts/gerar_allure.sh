#!/bin/bash
# ============================================================================
# Script: gerar_allure.sh
# Purpose: Generate Allure HTML report and open in browser
# Usage: ./gerar_allure.sh
# ============================================================================

echo ""
echo "========================================"
echo "  Allure Report Generator"
echo "========================================"
echo ""

# Check if Allure CLI is installed
if ! command -v allure &> /dev/null; then
    echo "[ERROR] Allure CLI not found!"
    echo ""
    echo "Please install Allure using one of these methods:"
    echo "  1. Using Homebrew (macOS): brew install allure"
    echo "  2. Using apt (Ubuntu/Debian): sudo apt-add-repository ppa:qameta/allure && sudo apt-get update && sudo apt-get install allure"
    echo "  3. Using npm: npm install -g allure-commandline"
    echo "  4. Manual download: https://docs.qameta.io/allure/#_installing_a_commandline"
    echo ""
    exit 1
fi

# Check if allure-results directory exists
if [ ! -d "reports/allure-results" ]; then
    echo "[ERROR] Directory 'reports/allure-results' not found!"
    echo ""
    echo "Please run tests first to generate results:"
    echo "  pytest tests/ --alluredir=reports/allure-results"
    echo ""
    exit 1
fi

# Check if there are any result files
if [ -z "$(ls -A reports/allure-results/*.json 2>/dev/null)" ]; then
    echo "[WARNING] No test results found in 'reports/allure-results'!"
    echo ""
    echo "Please run tests first:"
    echo "  pytest tests/ --alluredir=reports/allure-results"
    echo ""
    exit 1
fi

echo "[INFO] Generating Allure report..."
echo ""

# Generate the report
allure generate --clean reports/allure-results -o reports/allure-report

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to generate Allure report!"
    echo ""
    echo "Troubleshooting:"
    echo "  - Check if allure-results contains valid JSON files"
    echo "  - Try running: allure generate --clean reports/allure-results"
    echo "  - Check Allure version: allure --version"
    echo ""
    exit 1
fi

echo ""
echo "[SUCCESS] Allure report generated successfully!"
echo ""
echo "Report location: reports/allure-report/index.html"
echo ""
echo "Opening report in browser..."
echo ""

# Open the report in default browser (cross-platform)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open reports/allure-report/index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open reports/allure-report/index.html
    elif command -v gnome-open &> /dev/null; then
        gnome-open reports/allure-report/index.html
    else
        echo "[INFO] Please open reports/allure-report/index.html manually"
    fi
else
    echo "[INFO] Please open reports/allure-report/index.html manually"
fi

echo ""
echo "========================================"
echo "  Report opened in browser"
echo "========================================"
echo ""
