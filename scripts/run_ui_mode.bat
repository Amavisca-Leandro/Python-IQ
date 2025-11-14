@echo off
REM Script para executar testes em modo UI (interface gráfica)

echo ========================================
echo   Playwright UI Mode
echo ========================================
echo.
echo Abrindo interface grafica para testes...
echo.
echo Dicas:
echo - Clique em qualquer teste para executar
echo - Use "Pick Locator" para inspecionar elementos
echo - Veja o navegador e codigo lado a lado
echo.

REM Ir para o diretório raiz do projeto
cd /d "%~dp0.."

REM Ativar ambiente virtual se existir
if exist .venv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
)

REM Verificar se pytest está instalado
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: pytest nao esta instalado!
    echo Instalando pytest...
    pip install pytest pytest-playwright
    playwright install chromium
)

REM Executar testes de exemplo
echo.
echo Executando testes de exemplo...
echo.
python -m pytest tests/examples/ --headed --slowmo=500 -v

echo.
echo ========================================
echo Pressione qualquer tecla para sair...
pause > nul
