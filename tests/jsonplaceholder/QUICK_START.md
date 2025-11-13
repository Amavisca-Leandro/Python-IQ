# JSONPlaceholder API Tests - Quick Start Guide

## 🚀 Execução Rápida

### Executar Todos os Testes
```bash
pytest tests/jsonplaceholder/ -v
```

### Executar com Relatório HTML
```bash
pytest tests/jsonplaceholder/ -v --html=reports/jsonplaceholder_report.html --self-contained-html
```

### Executar Testes Smoke (Rápido)
```bash
pytest tests/jsonplaceholder/ -m smoke -v
```

### Executar Testes de Performance
```bash
pytest tests/jsonplaceholder/ -m performance -v
```

## 📊 Gerar Relatórios

### Relatório HTML Aprimorado
```bash
python scripts/generate_jsonplaceholder_report.py
```

Abre: `reports/jsonplaceholder_enhanced_report.html`

### Relatório de Métricas
Gerado automaticamente após cada execução em:
```
reports/jsonplaceholder_metrics.txt
```

## 🎯 Comandos Úteis

### Por Categoria
```bash
# Smoke tests
pytest tests/jsonplaceholder/ -m smoke -v

# CRUD tests
pytest tests/jsonplaceholder/ -m crud -v

# Validation tests
pytest tests/jsonplaceholder/ -m validation -v

# Filter tests
pytest tests/jsonplaceholder/ -m filters -v

# Performance tests
pytest tests/jsonplaceholder/ -m performance -v
```

### Por Recurso
```bash
# Posts
pytest tests/jsonplaceholder/test_posts.py -v

# Users
pytest tests/jsonplaceholder/test_users.py -v

# Comments
pytest tests/jsonplaceholder/test_comments.py -v

# Todos
pytest tests/jsonplaceholder/test_todos.py -v

# Albums
pytest tests/jsonplaceholder/test_albums.py -v

# Filters
pytest tests/jsonplaceholder/test_filters.py -v

# Performance
pytest tests/jsonplaceholder/test_performance.py -v
```

### Execução Paralela (Mais Rápido)
```bash
pytest tests/jsonplaceholder/ -v -n auto
```

## 📈 Visualizar Resultados

1. **Relatório HTML Padrão**: Abra `reports/jsonplaceholder_report.html` no navegador
2. **Relatório Aprimorado**: Abra `reports/jsonplaceholder_enhanced_report.html` no navegador
3. **Métricas**: Visualize `reports/jsonplaceholder_metrics.txt` em qualquer editor de texto

## 🔍 Debugging

### Executar um Teste Específico
```bash
pytest tests/jsonplaceholder/test_posts.py::test_get_posts_returns_200_and_list -v
```

### Ver Output Detalhado
```bash
pytest tests/jsonplaceholder/ -v -s
```

### Ver Traceback Completo
```bash
pytest tests/jsonplaceholder/ -v --tb=long
```

## 📚 Mais Informações

Consulte o [README.md](README.md) completo para documentação detalhada.
