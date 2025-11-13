$env:GIT_PAGER = 'type'
git add -A
git commit -m "feat: Add VS Code Test Explorer integration with JSONPlaceholder API tests

- Add .vscode configuration (settings, launch, extensions)
- Add Test Explorer documentation in Portuguese  
- Add 93 functional tests for JSONPlaceholder API
- Add JSONPlaceholder client and schemas
- Add metrics plugin and report generator
- Remove mock backend tests (non-functional)
- Update README with Test Explorer section
- Fix pytest configuration issues"

Write-Host ""
Write-Host "Commit criado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "Para enviar ao repositorio remoto, execute:" -ForegroundColor Yellow
Write-Host "git push origin main" -ForegroundColor Cyan
