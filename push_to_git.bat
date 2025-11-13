@echo off
echo Fechando processos do git...
taskkill /F /IM git.exe /T 2>nul
taskkill /F /IM less.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo Fazendo push para o repositorio...
git push origin main

echo.
echo Pressione qualquer tecla para fechar...
pause >nul
