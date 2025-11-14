@echo off
REM Script para gerar relatórios de métricas de testes
REM Usage: gerar_relatorio_metricas.bat [days] [format]

setlocal

set DAYS=%1
set FORMAT=%2

if "%DAYS%"=="" set DAYS=30
if "%FORMAT%"=="" set FORMAT=all

echo ========================================
echo Gerando Relatorios de Metricas
echo ========================================
echo Periodo: Ultimos %DAYS% dias
echo Formato: %FORMAT%
echo.

python scripts\generate_metrics_report.py --days %DAYS% --format %FORMAT% --show-flaky --show-trends

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Relatorios gerados com sucesso!
    echo ========================================
    echo.
    echo Abrir relatorio HTML? (S/N)
    set /p OPEN_HTML=
    if /i "%OPEN_HTML%"=="S" (
        start reports\metrics\quality_dashboard.html
    )
) else (
    echo.
    echo ========================================
    echo Erro ao gerar relatorios!
    echo ========================================
)

endlocal
pause
