@echo off
REM ============================================================================
REM Script: allure_server.bat
REM Purpose: Start Allure local server for live report viewing
REM Usage: allure_server.bat
REM ============================================================================

echo.
echo ========================================
echo   Allure Server Launcher
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

echo [INFO] Starting Allure server on port 4040...
echo.
echo Server will open automatically in your browser.
echo.
echo To stop the server, press Ctrl+C in this window.
echo.
echo ========================================
echo.

REM Start Allure server on port 4040
allure serve reports\allure-results -p 4040

REM This line will only execute if the server stops
echo.
echo [INFO] Allure server stopped.
echo.
pause
