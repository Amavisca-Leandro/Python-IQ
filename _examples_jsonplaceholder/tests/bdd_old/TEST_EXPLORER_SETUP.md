# Como Visualizar Testes BDD no Test Explorer

## Problema

Os testes BDD não estão aparecendo no Test Explorer do Kiro IDE.

## Verificação

Os testes BDD estão corretamente implementados e podem ser descobertos pelo pytest:

```bash
pytest --collect-only tests/bdd/ -q
```

**Resultado:** 92 testes coletados com sucesso ✅

## Solução: Atualizar Test Explorer

### Opção 1: Recarregar Test Explorer (Recomendado)

1. **Abrir Command Palette:**
   - Windows/Linux: `Ctrl+Shift+P`
   - Mac: `Cmd+Shift+P`

2. **Procurar por:** `Test: Refresh Tests` ou `Reload Window`

3. **Executar o comando**

### Opção 2: Recarregar Janela do Kiro

1. **Abrir Command Palette:**
   - Windows/Linux: `Ctrl+Shift+P`
   - Mac: `Cmd+Shift+P`

2. **Procurar por:** `Developer: Reload Window`

3. **Executar o comando**

### Opção 3: Reiniciar Kiro IDE

1. Fechar completamente o Kiro IDE
2. Reabrir o projeto
3. Aguardar a indexação completa

### Opção 4: Forçar Descoberta de Testes

1. **Abrir o painel Test Explorer**
2. **Clicar no ícone de refresh/reload** (geralmente no topo do painel)
3. **Aguardar a descoberta dos testes**

## Estrutura dos Testes BDD

Após a atualização, você deverá ver a seguinte estrutura no Test Explorer:

```
tests/
└── bdd/
    ├── test_posts_api.py (16 testes)
    │   ├── test_get_all_posts
    │   ├── test_create_a_new_post
    │   ├── test_get_post_by_id[1-200]
    │   ├── test_get_post_by_id[50-200]
    │   ├── test_get_post_by_id[100-200]
    │   ├── test_get_specific_post_and_validate_structure
    │   ├── test_update_an_existing_post
    │   ├── test_delete_a_post
    │   ├── test_get_posts_by_user_id
    │   ├── test_validate_post_fields_for_different_posts[1-1]
    │   ├── test_validate_post_fields_for_different_posts[11-2]
    │   ├── test_validate_post_fields_for_different_posts[21-3]
    │   ├── test_validate_post_fields_for_different_posts[31-4]
    │   ├── test_validate_post_fields_for_different_posts[41-5]
    │   ├── test_create_post_with_all_fields_and_validate_response
    │   └── test_verify_posts_list_contains_multiple_items
    │
    ├── test_users_api.py (30 testes)
    │   ├── test_get_all_users
    │   ├── test_get_user_by_id[1-200]
    │   ├── test_get_user_by_id[5-200]
    │   ├── test_get_user_by_id[10-200]
    │   ├── test_get_specific_user_and_validate_structure
    │   ├── test_create_a_new_user
    │   ├── test_update_an_existing_user
    │   ├── test_delete_a_user
    │   ├── test_validate_user_fields_for_different_users[1-Leanne Graham]
    │   ├── test_validate_user_fields_for_different_users[2-Ervin Howell]
    │   ├── test_validate_user_fields_for_different_users[3-Clementine Bauch]
    │   ├── test_validate_user_fields_for_different_users[4-Patricia Lebsack]
    │   ├── test_validate_user_fields_for_different_users[5-Chelsey Dietrich]
    │   ├── test_create_user_with_all_required_fields_and_validate_response
    │   ├── test_verify_users_list_contains_multiple_items
    │   ├── test_validate_user_address_structure
    │   ├── test_validate_user_company_structure
    │   ├── test_validate_multiple_user_ids_return_success[1-10]
    │   ├── test_update_different_users_with_new_data[1-3]
    │   ├── test_get_users_and_verify_email_format
    │   └── test_create_user_with_minimal_required_fields
    │
    ├── test_data_management.py (14 testes)
    │   ├── test_create_and_query_test_user
    │   ├── test_create_test_user_with_username
    │   ├── test_create_test_user_with_profile
    │   ├── test_create_multiple_test_users
    │   ├── test_validate_database_state_after_api_operation
    │   ├── test_demonstrate_test_data_cleanup
    │   ├── test_execute_custom_sql_query
    │   ├── test_query_users_by_field_value
    │   ├── test_create_test_data_from_table_specification
    │   ├── test_validate_database_field_values
    │   ├── test_endtoend_database_and_api_integration
    │   ├── test_query_user_by_id
    │   ├── test_verify_nonexistent_user
    │   └── test_create_user_and_validate_all_fields
    │
    ├── test_end_to_end_integration.py (9 testes)
    │   ├── test_create_user_in_database_and_validate_via_api_calls
    │   ├── test_multistep_api_workflow_with_context_data_sharing
    │   ├── test_database_state_validation_after_api_operations
    │   ├── test_complex_workflow_with_multiple_database_entities_and_api_calls
    │   ├── test_sequential_api_calls_with_database_validation_at_each_step
    │   ├── test_full_crud_cycle_with_database_and_api_integration
    │   ├── test_demonstrate_bdd_context_usage_for_data_sharing_between_steps
    │   ├── test_error_handling_and_validation_in_integrated_workflow
    │   └── test_bulk_operations_with_database_and_api
    │
    ├── test_database_steps.py (5 testes)
    │   ├── test_create_and_query_a_test_user_by_email
    │   ├── test_create_and_query_a_test_user_by_username
    │   ├── test_create_user_with_profile
    │   ├── test_create_multiple_users
    │   └── test_query_nonexistent_user
    │
    ├── test_api_steps_validation.py (3 testes)
    │   ├── test_get_request_with_response_validation
    │   ├── test_post_request_with_data_preparation
    │   └── test_get_list_with_validation
    │
    └── test_explorer_verification.py (13 testes)
        ├── TestExplorerDiscovery
        │   ├── test_scenarios_discovered_as_individual_items
        │   ├── test_scenarios_grouped_by_feature_file
        │   ├── test_tags_displayed_correctly
        │   └── test_scenario_outlines_expanded
        ├── TestExplorerExecution
        │   ├── test_individual_scenario_execution
        │   ├── test_debugging_support
        │   ├── test_results_display_correctly
        │   └── test_marker_filtering_works
        ├── TestExplorerIntegration
        │   ├── test_feature_file_structure_valid
        │   ├── test_test_files_linked_to_features
        │   ├── test_parallel_execution_support
        │   └── test_error_reporting_in_explorer
        └── TestExplorerDocumentation
            └── test_readme_contains_explorer_instructions
```

**Total: 92 testes BDD**

## Verificação Manual

Para confirmar que os testes estão funcionando, execute no terminal:

```bash
# Listar todos os testes BDD
pytest --collect-only tests/bdd/ -q

# Executar um teste específico
pytest tests/bdd/test_posts_api.py::test_get_all_posts -v

# Executar todos os testes BDD
pytest tests/bdd/ -v

# Executar testes com marcador específico
pytest tests/bdd/ -m smoke -v
```

## Recursos do Test Explorer para BDD

Após os testes aparecerem no Test Explorer, você poderá:

### 1. Executar Testes Individuais
- Clique no ▶️ ao lado de qualquer teste
- Executa apenas aquele cenário específico

### 2. Executar Grupos de Testes
- Clique no ▶️ ao lado de um arquivo de teste
- Executa todos os cenários daquele arquivo

### 3. Filtrar por Tags/Markers
- Use o filtro do Test Explorer
- Filtre por: `@smoke`, `@api`, `@crud`, `@database`, etc.

### 4. Debugar Cenários
- Clique no 🐛 ao lado de um teste
- Defina breakpoints nos step definitions em `tests/bdd/steps/`
- Inspecione variáveis durante a execução

### 5. Ver Resultados
- ✅ Verde: Teste passou
- ❌ Vermelho: Teste falhou
- ⏱️ Tempo de execução exibido
- 📋 Mensagens de erro detalhadas

## Arquivos de Feature Correspondentes

Cada arquivo de teste corresponde a um arquivo `.feature`:

| Arquivo de Teste | Arquivo Feature |
|-----------------|-----------------|
| `test_posts_api.py` | `features/api/posts.feature` |
| `test_users_api.py` | `features/api/users.feature` |
| `test_data_management.py` | `features/database/data_management.feature` |
| `test_end_to_end_integration.py` | `features/integration/end_to_end.feature` |

## Troubleshooting

### Problema: Testes ainda não aparecem

**Solução 1:** Verificar configuração do Python
```bash
# Verificar se o pytest está instalado
pytest --version

# Verificar se pytest-bdd está instalado
pip list | grep pytest-bdd
```

**Solução 2:** Limpar cache do pytest
```bash
# Remover cache
rm -rf .pytest_cache
rm -rf tests/bdd/__pycache__

# Windows
rmdir /s /q .pytest_cache
rmdir /s /q tests\bdd\__pycache__
```

**Solução 3:** Verificar workspace settings
- Certifique-se de que o diretório `tests/` está incluído no workspace
- Verifique se não há exclusões no `.gitignore` ou settings

### Problema: Testes aparecem mas não executam

**Solução:** Verificar dependências
```bash
# Instalar dependências necessárias
pip install -r requirements.txt

# Verificar instalação do pytest-bdd
pip install pytest-bdd
```

### Problema: Erros ao executar testes

**Solução:** Verificar configuração do ambiente
```bash
# Verificar arquivo .env existe
ls -la .env

# Verificar pytest.ini está correto
cat pytest.ini
```

## Suporte

Se os testes ainda não aparecerem após seguir todos os passos:

1. Verifique os logs do Kiro IDE
2. Abra o Developer Console (Help > Toggle Developer Tools)
3. Procure por erros relacionados a "test discovery" ou "pytest"
4. Compartilhe os logs para análise

## Comandos Úteis

```bash
# Descobrir testes
pytest --collect-only tests/bdd/

# Executar com verbose
pytest tests/bdd/ -v

# Executar com markers
pytest tests/bdd/ -m smoke

# Executar arquivo específico
pytest tests/bdd/test_posts_api.py

# Executar teste específico
pytest tests/bdd/test_posts_api.py::test_get_all_posts

# Executar com debug
pytest tests/bdd/test_posts_api.py::test_get_all_posts -v --pdb

# Executar em paralelo
pytest tests/bdd/ -n auto
```

## Conclusão

Os testes BDD estão corretamente implementados e funcionais. Após recarregar o Test Explorer, você deverá ver todos os 92 testes organizados por arquivo e prontos para execução.
