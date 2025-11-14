@echo off
REM ============================================================================
REM Script: gerar_allure.bat
REM Purpose: Generate Allure HTML report and open in browser
REM Usage: gerar_allure.bat
REM ============================================================================

echo.
echo ========================================
echo   Allure Report Generator
echo ========================================
echo.

REM Check if Allure CLI is installed
where allure >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Allure CLI not found!
    echo.
    echo Please install Allure using one of these methods:
    echo   1. Using Scoop: scoop install allure
    echo   2. Using npm: npm install -g allure-commandline
    echo   3. Manual download: https://docs.qameta.io/allure/#_installing_a_commandline
    echo.
    pause
    exit /b 1
)

REM Check if allure-results directory exists
if not exist "reports\allure-results" (
    echo [ERROR] Directory 'reports\allure-results' not found!
    echo.
    echo Please run tests first to generate results:
    echo   pytest tests/ --alluredir=reports/allure-results
    echo.
    pause
    exit /b 1
)

REM Check if there are any result files
dir /b "reports\allure-results\*.json" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] No test results found in 'reports\allure-results'!
    echo.
    echo Please run tests first:
    echo   pytest tests/ --alluredir=reports/allure-results
    echo.
    pause
    exit /b 1
)

echo [INFO] Generating Allure report...
echo.

REM Generate the report
allure generate --clean reports\allure-results -o reports\allure-report

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to generate Allure report!
    echo.
    echo Troubleshooting:
    echo   - Check if allure-results contains valid JSON files
    echo   - Try running: allure generate --clean reports\allure-results
    echo   - Check Allure version: allure --version
    echo.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Allure report generated successfully!
echo.
echo Report location: reports\allure-report\index.html
echo.
echo Opening report in browser...
echo.

REM Open the report in default browser
start "" "reports\allure-report\index.html"

echo.
echo ========================================
echo   Report opened in browser
echo ========================================
echo.
pause
