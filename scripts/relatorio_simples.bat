@echo off
REM Script simples e robusto para gerar relatório

echo ========================================
echo   Gerando Relatorio HTML
echo ========================================
echo.

REM Ir para raiz do projeto
cd /d "%~dp0.."

REM Mostrar diretório atual
echo Diretorio atual: %CD%
echo.

REM Ativar ambiente virtual
if exist .venv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
    echo Ambiente ativado!
) else (
    echo AVISO: Ambiente virtual nao encontrado!
    echo Usando Python global...
)

echo.
echo Verificando instalacao do pytest-html...
python -m pip show pytest-html >nul 2>&1
if errorlevel 1 (
    echo Instalando pytest-html...
    python -m pip install pytest-html
)

REM Criar pasta reports
if not exist reports mkdir reports

echo.
echo ========================================
echo Executando testes...
echo ========================================
echo.

REM Executar testes com caminho absoluto
python -m pytest "%CD%\tests\examples" --html="%CD%\reports\relatorio.html" --self-contained-html -v -s

echo.
echo ========================================

REM Verificar se relatório foi criado
if exist "%CD%\reports\relatorio.html" (
    echo.
    echo ✅ Relatorio gerado com sucesso!
    echo.
    echo Abrindo relatorio...
    start "" "%CD%\reports\relatorio.html"
) else (
    echo.
    echo ❌ ERRO: Relatorio nao foi gerado!
    echo.
    echo Verifique os erros acima.
)

echo.
echo Arquivo: %CD%\reports\relatorio.html
echo.
pause
