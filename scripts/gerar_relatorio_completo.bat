@echo off
REM Script para gerar relatório HTML completo de TODOS os testes

echo ========================================
echo   Relatorio Completo - Todos os Testes
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

REM Executar TODOS os testes e gerar relatório
echo.
echo Executando TODOS os testes...
echo Isso pode demorar alguns minutos...
echo.
python -m pytest tests/ --html=reports/relatorio_completo.html --self-contained-html -v

REM Verificar se relatório foi gerado
if exist reports\relatorio_completo.html (
    echo.
    echo ========================================
    echo Relatorio completo gerado com sucesso!
    echo Abrindo no navegador...
    echo ========================================
    echo.
    start reports\relatorio_completo.html
) else (
    echo.
    echo ERRO: Relatorio nao foi gerado!
    echo Verifique os erros acima.
)

echo.
echo Arquivo salvo em: reports\relatorio_completo.html
echo.
pause
