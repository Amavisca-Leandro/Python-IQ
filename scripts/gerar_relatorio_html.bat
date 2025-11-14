@echo off
REM Script para executar testes e gerar relatório HTML

echo ========================================
echo   Gerando Relatório HTML
echo ========================================
echo.

REM Ativar ambiente virtual se existir
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Instalar pytest-html se não estiver instalado
pip show pytest-html >nul 2>&1
if errorlevel 1 (
    echo Instalando pytest-html...
    pip install pytest-html
)

REM Criar pasta de relatórios se não existir
if not exist reports mkdir reports

REM Executar testes e gerar relatório
echo.
echo Executando testes...
pytest tests/examples/ --html=reports/relatorio_testes.html --self-contained-html -v

REM Abrir relatório no navegador
if exist reports\relatorio_testes.html (
    echo.
    echo ========================================
    echo Relatório gerado com sucesso!
    echo Abrindo no navegador...
    echo ========================================
    start reports\relatorio_testes.html
) else (
    echo.
    echo ERRO: Relatório não foi gerado!
)

echo.
pause
