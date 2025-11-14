@echo off
REM Script simples para testar o Google

echo ========================================
echo   Teste Simples - Google
echo ========================================
echo.
echo Executando teste do Google...
echo O navegador vai abrir automaticamente!
echo.

REM Ir para o diretório raiz
cd /d "%~dp0.."

REM Ativar ambiente virtual se existir
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Executar teste específico
python -m pytest tests/examples/test_exemplo_basico.py::test_abrir_google --headed --slowmo=1000 -v -s

echo.
echo ========================================
echo Teste concluido!
echo Pressione qualquer tecla para sair...
pause > nul
