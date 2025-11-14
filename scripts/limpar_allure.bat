@echo off
REM ============================================================================
REM Script: limpar_allure.bat
REM Purpose: Clean old Allure results and reports
REM Usage: limpar_allure.bat
REM ============================================================================

echo.
echo ========================================
echo   Allure Cleanup Utility
echo ========================================
echo.

echo This will delete:
echo   - All files in reports\allure-results\
echo   - All files in reports\allure-report\
echo.

REM Prompt for confirmation
set /p confirm="Are you sure you want to continue? (Y/N): "

if /i not "%confirm%"=="Y" (
    echo.
    echo [INFO] Cleanup cancelled.
    echo.
    pause
    exit /b 0
)

echo.
echo [INFO] Starting cleanup...
echo.

set cleaned_results=0
set cleaned_report=0

REM Clean allure-results directory
if exist "reports\allure-results" (
    echo [INFO] Cleaning allure-results directory...
    del /q "reports\allure-results\*.*" 2>nul
    for /d %%p in ("reports\allure-results\*") do rmdir "%%p" /s /q 2>nul
    set cleaned_results=1
    echo [OK] Cleaned allure-results
) else (
    echo [INFO] Directory 'reports\allure-results' does not exist
)

echo.

REM Clean allure-report directory
if exist "reports\allure-report" (
    echo [INFO] Cleaning allure-report directory...
    del /q "reports\allure-report\*.*" 2>nul
    for /d %%p in ("reports\allure-report\*") do rmdir "%%p" /s /q 2>nul
    set cleaned_report=1
    echo [OK] Cleaned allure-report
) else (
    echo [INFO] Directory 'reports\allure-report' does not exist
)

echo.
echo ========================================
echo   Cleanup Summary
echo ========================================
echo.

if %cleaned_results%==1 (
    echo [✓] Allure results cleaned
) else (
    echo [−] No allure results to clean
)

if %cleaned_report%==1 (
    echo [✓] Allure report cleaned
) else (
    echo [−] No allure report to clean
)

echo.
echo [SUCCESS] Cleanup completed!
echo.
echo You can now run tests to generate fresh results:
echo   pytest tests/ --alluredir=reports/allure-results
echo.
pause
