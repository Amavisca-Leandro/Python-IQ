@echo off
REM Menu interativo para gerar relatórios

:MENU
cls
echo ========================================
echo   Menu de Relatorios
echo ========================================
echo.
echo Escolha o tipo de relatorio:
echo.
echo 1. Testes de Exemplo (tests/examples/)
echo 2. Testes de Frontend (tests/frontend/)
echo 3. Testes de API (tests/jsonplaceholder/)
echo 4. Testes de Integracao (tests/integration/)
echo 5. TODOS os testes
echo 6. Relatorio Allure (Profissional)
echo 0. Sair
echo.
echo ========================================
set /p opcao="Digite o numero da opcao: "

if "%opcao%"=="1" goto EXAMPLES
if "%opcao%"=="2" goto FRONTEND
if "%opcao%"=="3" goto API
if "%opcao%"=="4" goto INTEGRATION
if "%opcao%"=="5" goto TODOS
if "%opcao%"=="6" goto ALLURE
if "%opcao%"=="0" goto FIM
goto MENU

:EXAMPLES
cls
echo Gerando relatorio dos testes de exemplo...
cd /d "%~dp0.."
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python -m pytest tests/examples/ --html=reports/relatorio_examples.html --self-contained-html -v
if exist reports\relatorio_examples.html start reports\relatorio_examples.html
pause
goto MENU

:FRONTEND
cls
echo Gerando relatorio dos testes de frontend...
cd /d "%~dp0.."
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python -m pytest tests/frontend/ --html=reports/relatorio_frontend.html --self-contained-html -v
if exist reports\relatorio_frontend.html start reports\relatorio_frontend.html
pause
goto MENU

:API
cls
echo Gerando relatorio dos testes de API...
cd /d "%~dp0.."
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python -m pytest tests/jsonplaceholder/ --html=reports/relatorio_api.html --self-contained-html -v
if exist reports\relatorio_api.html start reports\relatorio_api.html
pause
goto MENU

:INTEGRATION
cls
echo Gerando relatorio dos testes de integracao...
cd /d "%~dp0.."
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python -m pytest tests/integration/ --html=reports/relatorio_integration.html --self-contained-html -v
if exist reports\relatorio_integration.html start reports\relatorio_integration.html
pause
goto MENU

:TODOS
cls
echo Gerando relatorio completo (TODOS os testes)...
echo Isso pode demorar alguns minutos...
cd /d "%~dp0.."
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python -m pytest tests/ --html=reports/relatorio_completo.html --self-contained-html -v
if exist reports\relatorio_completo.html start reports\relatorio_completo.html
pause
goto MENU

:ALLURE
cls
echo Gerando relatorio Allure...
cd /d "%~dp0.."
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
pip show allure-pytest >nul 2>&1
if errorlevel 1 (
    echo Instalando allure-pytest...
    pip install allure-pytest
)
python -m pytest tests/examples/ --alluredir=reports/allure-results -v
echo.
echo Para ver o relatorio, execute:
echo allure serve reports/allure-results
echo.
pause
goto MENU

:FIM
echo.
echo Ate logo!
exit
