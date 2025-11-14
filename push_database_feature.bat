@echo off
echo ========================================
echo Push Database Integration Feature
echo ========================================
echo.
echo Esta feature inclui 7 commits:
echo.
echo 1. feat(database): enhance DatabaseManager with ORM data creation method
echo 2. feat(database): add convenience methods and validations to SQLAlchemy models
echo 3. feat(database): implement complex scenarios and automatic cleanup in TestDataFactory
echo 4. test(database): add comprehensive integration tests for database framework
echo 5. docs(database): add comprehensive usage documentation for database framework
echo 6. docs(database): add implementation summary for task 4
echo 7. chore(specs): update task 4 status to completed
echo.
echo ========================================
echo.

set /p confirm="Deseja fazer push para origin/main? (S/N): "

if /i "%confirm%"=="S" (
    echo.
    echo Fazendo push...
    git push origin main
    echo.
    echo ========================================
    echo Push concluido com sucesso!
    echo ========================================
) else (
    echo.
    echo Push cancelado.
)

echo.
pause
