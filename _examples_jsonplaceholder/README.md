# 📚 Exemplos de Testes - JSONPlaceholder API

## 📋 Sobre

Esta pasta contém os **testes de exemplo** originais do framework python-iq que usavam a API pública JSONPlaceholder para demonstração.

Estes testes foram movidos para esta pasta de exemplos para **evitar confusão** com os testes reais dos projetos em produção.

## 🎯 Propósito

Estes testes servem como:

- ✅ **Exemplos de implementação** de testes BDD, API e UI
- ✅ **Referência de padrões** do framework
- ✅ **Material de aprendizado** para novos desenvolvedores
- ✅ **Testes de demonstração** que funcionam sem dependências externas

## 📁 Conteúdo

```
_examples_jsonplaceholder/
├── tests/
│   ├── functional/         # Testes funcionais de API e UI
│   │   ├── backend/        # Testes de API (posts, users, comments, etc.)
│   │   └── frontend/       # Testes de UI (login, user journey)
│   ├── jsonplaceholder/    # Testes de performance
│   ├── system/             # Testes de integração e exploração
│   └── bdd/                # Testes BDD com features Gherkin
│       ├── features/       # Arquivos .feature
│       └── steps/          # Step definitions
└── README.md
```

## 🚀 Como Usar os Exemplos

### Executar testes de exemplo

```bash
# Executar testes de API de exemplo
pytest _examples_jsonplaceholder/tests/functional/backend/ -v

# Executar testes BDD de exemplo
pytest _examples_jsonplaceholder/tests/functional/backend/test_posts_api.py -v

# Executar com Allure
pytest _examples_jsonplaceholder/tests/functional/backend/ --alluredir=reports/examples
allure serve reports/examples
```

### Estudar os padrões

1. **API Testing Pattern**:
   - Ver `tests/functional/backend/test_posts_api.py`
   - Exemplo de uso do APIClient
   - Validação de schemas com Pydantic

2. **BDD Pattern**:
   - Ver `tests/bdd/features/api/posts.feature`
   - Step definitions em `tests/bdd/steps/`
   - Integração com Allure

3. **UI Testing Pattern**:
   - Ver `tests/functional/frontend/test_login_ui.py`
   - Page Object Model
   - Playwright automation

## ⚠️ Importante

- **NÃO modificar** estes arquivos - eles são apenas para referência
- Para testes reais, use a estrutura `projects/` no diretório raiz
- Estes testes usam a API pública JSONPlaceholder que pode estar indisponível

## 🔗 API JSONPlaceholder

Os testes usam: https://jsonplaceholder.typicode.com/

Endpoints disponíveis:
- `/posts` - Posts de exemplo
- `/users` - Usuários de exemplo
- `/comments` - Comentários
- `/todos` - Lista de tarefas
- `/albums` - Álbuns de fotos

## 📚 Documentação do Framework

Para documentação completa do framework python-iq, consulte:
- [docs/INDEX.md](../docs/INDEX.md)
- [docs/architecture/MULTI_PROJECT_GUIDE.md](../docs/architecture/MULTI_PROJECT_GUIDE.md)
- [CLAUDE.md](../CLAUDE.md)

## 🎓 Próximos Passos

Se você está aprendendo o framework:

1. ✅ Explore estes exemplos para entender os padrões
2. ✅ Leia a documentação do framework
3. ✅ Crie seus testes no diretório `projects/seu-projeto/`
4. ✅ Use os exemplos como referência, mas não os modifique

---

**Nota**: Estes testes foram movidos em 2025-01 para manter o framework organizado e focado nos projetos reais em `projects/`.
