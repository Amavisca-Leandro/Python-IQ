@echo off
REM Script de diagnóstico para verificar configuração

echo ========================================
echo   Diagnostico do Ambiente
echo ========================================
echo.

cd /d "%~dp0.."

echo 1. Diretorio atual:
echo %CD%
echo.

echo 2. Verificando Python:
python --version
echo.

echo 3. Verificando pytest:
python -m pytest --version
echo.

echo 4. Verificando pytest-html:
python -m pip show pytest-html
echo.

echo 5. Verificando playwright:
python -m pip show playwright
echo.

echo 6. Listando testes disponiveis:
python -m pytest tests/examples/ --collect-only
echo.

echo 7. Verificando estrutura de pastas:
dir tests\examples
echo.

echo 8. Pacotes instalados:
python -m pip list | findstr "pytest playwright"
echo.

echo ========================================
echo Diagnostico concluido!
echo ========================================
pause
