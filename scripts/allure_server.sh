#!/bin/bash
# ============================================================================
# Script: allure_server.sh
# Purpose: Start Allure local server for live report viewing
# Usage: ./allure_server.sh
# ============================================================================

echo ""
echo "========================================"
echo "  Allure Server Launcher"
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

echo "[INFO] Starting Allure server on port 4040..."
echo ""
echo "Server will open automatically in your browser."
echo ""
echo "To stop the server, press Ctrl+C in this terminal."
echo ""
echo "========================================"
echo ""

# Start Allure server on port 4040
allure serve reports/allure-results -p 4040

# This line will only execute if the server stops
echo ""
echo "[INFO] Allure server stopped."
echo ""
