@echo off
REM ============================================================================
REM Allure Report Validation Script
REM ============================================================================
REM This script validates that the Allure report contains all expected features
REM ============================================================================

echo.
echo ============================================================================
echo ALLURE REPORT VALIDATION
echo ============================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8 or higher
    exit /b 1
)

REM Run validation script
python scripts/validate_allure_report.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Validation completed successfully!
) else (
    echo.
    echo [WARNING] Some validation checks failed
    echo Review the output above for details
)

echo.
pause
