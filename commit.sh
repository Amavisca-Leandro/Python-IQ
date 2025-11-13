#!/bin/bash

echo "Criando commit..."

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

echo ""
echo "Commit criado com sucesso!"
echo ""
echo "Para enviar ao repositorio remoto, execute:"
echo "git push origin main"
