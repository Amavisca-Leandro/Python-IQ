@echo off
echo Criando commits para o projeto...

REM Commit 1: VS Code Test Explorer configuration
git add .vscode\settings.json .vscode\launch.json .vscode\extensions.json
git commit -m "feat: Add VS Code Test Explorer configuration"

REM Commit 2: Test Explorer documentation
git add docs\test-explorer-guide.md
git commit -m "docs: Add comprehensive Test Explorer guide in Portuguese"

REM Commit 3: JSONPlaceholder API tests
git add tests\jsonplaceholder\ core\clients\
git commit -m "feat: Add 93 functional tests for JSONPlaceholder API"

REM Commit 4: Metrics and reporting
git add scripts\generate_jsonplaceholder_report.py tests\jsonplaceholder\conftest_metrics.py
git commit -m "feat: Add metrics plugin and HTML report generator"

REM Commit 5: Remove mock tests
git add tests\
git commit -m "refactor: Remove non-functional mock backend tests"

REM Commit 6: Update documentation
git add README.md
git commit -m "docs: Update README with Test Explorer section"

REM Commit 7: Configuration fixes
git add tests\conftest.py .env
git commit -m "fix: Fix pytest configuration and environment setup"

REM Commit 8: Specs
git add .kiro\specs\
git commit -m "docs: Add project specs for Test Explorer and JSONPlaceholder tests"

echo.
echo Commits criados com sucesso!
echo.
echo Para enviar ao repositório remoto, execute:
echo git push origin main
