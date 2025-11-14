@echo off
REM Script para gerar relatório HTML dos testes de exemplo

echo ========================================
echo   Gerando Relatorio - Testes Examples
echo ========================================
echo.

REM Ir para o diretório raiz
cd /d "%~dp0.."

REM Ativar ambiente virtual
if exist .venv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
)

REM Instalar pytest-html se necessário
pip show pytest-html >nul 2>&1
if errorlevel 1 (
    echo Instalando pytest-html...
    pip install pytest-html
)

REM Criar pasta de relatórios
if not exist reports mkdir reports

REM Executar testes e gerar relatório
echo.
echo Executando testes de exemplo...
echo.
python -m pytest tests/examples/ --html=reports/relatorio_examples.html --self-contained-html -v --headed

REM Verificar se relatório foi gerado
if exist reports\relatorio_examples.html (
    echo.
    echo ========================================
    echo Relatorio gerado com sucesso!
    echo Abrindo no navegador...
    echo ========================================
    echo.
    start reports\relatorio_examples.html
) else (
    echo.
    echo ERRO: Relatorio nao foi gerado!
    echo Verifique os erros acima.
)

echo.
echo Arquivo salvo em: reports\relatorio_examples.html
echo.
pause
