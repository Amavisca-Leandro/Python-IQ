# -*- coding: utf-8 -*-
"""
Definições de passos para ações de API do Email Service.

Este módulo fornece steps para executar operações de API (When steps) para
gerenciamento de API Keys, Templates, Envio de Emails e Fila de Emails.

Steps incluem:
- API Keys: listar, criar, buscar, atualizar, deletar
- Templates: listar, criar, buscar, atualizar, deletar
- Email Sending: enviar emails simples, HTML, com template, com anexos
- Email Queue: adicionar fila, agendamento, cancelamento, status
"""

import allure
import logging
import json
from typing import Dict, Any
from pytest_bdd import when, parsers

logger = logging.getLogger(__name__)

allure.feature('Email Service - API Actions')
allure.story('API Requests')


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _parse_params_table(params_table: str) -> Dict[str, Any]:
    """
    Parse tabela de parâmetros Gherkin em dicionário.

    Args:
        params_table: String com tabela no formato Gherkin

    Returns:
        Dicionário com parâmetros
    """
    params = {}
    lines = params_table.strip().split('\n')

    for line in lines[1:]:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]

            if len(parts) >= 2:
                key = parts[0]
                value = parts[1]
                params[key] = _convert_value(value)

    return params


def _parse_filter_table(filter_table: str) -> Dict[str, Any]:
    """
    Parse tabela de filtros Gherkin em dicionário.

    Args:
        filter_table: String com tabela de filtros

    Returns:
        Dicionário com filtros
    """
    filters = {}
    lines = filter_table.strip().split('\n')

    for line in lines[1:]:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]

            if len(parts) >= 2:
                key = parts[0]
                value = parts[1]
                filters[key] = _convert_value(value)

    return filters


def _convert_value(value: str) -> Any:
    """
    Converter string em tipo Python apropriado.

    Handles:
    - Inteiros (e.g., "123" -> 123)
    - Floats (e.g., "12.34" -> 12.34)
    - Booleanos (e.g., "true" -> True)
    - Null/None (e.g., "null" -> None)
    - JSON objects/arrays (e.g., '{"key": "value"}' -> dict)
    - Strings (padrão)

    Args:
        value: String a converter

    Returns:
        Valor convertido com tipo apropriado
    """
    if value.lower() in ('null', 'none', ''):
        return None

    if value.lower() == 'true':
        return True

    if value.lower() == 'false':
        return False

    if value.startswith(('{', '[')):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


# ============================================================================
# API KEYS - ACTIONS
# ============================================================================

@when(parsers.parse('eu listo as API keys com os parâmetros:\n{params_table}'))
@allure.story('API Keys - List')
def listar_api_keys_com_parametros(bdd_context, email_service_client, params_table):
    """
    Listar API Keys com parâmetros de paginação e ordenação.

    Args:
        bdd_context: Contexto BDD
        email_service_client: Cliente do Email Service
        params_table: Tabela com parâmetros (page, limit, sort)

    Example:
        Quando eu listo as API keys com os parâmetros:
            | parametro | valor |
            | page      | 1     |
            | limit     | 10    |
    """
    with allure.step('Listar API keys com parâmetros'):
        try:
            params = _parse_params_table(params_table)

            logger.info(f'Listando API keys com parâmetros: {params}')

            response_data = email_service_client.list_api_keys(
                page=params.get('page', 1),
                limit=params.get('limit', 10),
                sort=params.get('sort'),
                filters=params.get('filters')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(params, indent=2),
                name='Request Params',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'API keys listadas com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao listar API keys: {e}')
            raise


@when(parsers.parse('eu listo as API keys filtrando por:\n{filter_table}'))
@allure.story('API Keys - Filter')
def listar_api_keys_filtrando(bdd_context, email_service_client, filter_table):
    """
    Listar API Keys com filtros.

    Args:
        bdd_context: Contexto BDD
        email_service_client: Cliente do Email Service
        filter_table: Tabela com filtros

    Example:
        Quando eu listo as API keys filtrando por:
            | filtro        | valor |
            | filter[isActive] | true  |
    """
    with allure.step('Listar API keys filtrando'):
        try:
            filters = _parse_filter_table(filter_table)

            logger.info(f'Listando API keys com filtros: {filters}')

            response_data = email_service_client.list_api_keys(filters=filters)

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(filters, indent=2),
                name='Filter Params',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'API keys filtradas com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao listar API keys filtradas: {e}')
            raise


@when('eu crio uma nova API key')
@allure.story('API Keys - Create')
def criar_api_key(bdd_context, email_service_client):
    """
    Criar uma nova API Key.

    Args:
        bdd_context: Contexto BDD (deve conter api_key_data)
        email_service_client: Cliente do Email Service

    Example:
        Dado eu tenho os dados da API key:
            | campo        | valor                |
            | name         | My API Key           |
            | expirationAt | 2025-12-31T23:59:59Z |
            | tier         | premium              |
        Quando eu crio uma nova API key
    """
    with allure.step('Criar nova API key'):
        try:
            data = bdd_context.api_key_data

            logger.info(f'Criando API key: {data.get("name")}')

            response_data = email_service_client.create_api_key(
                name=data['name'],
                expiration_at=data.get('expirationAt'),
                tier=data.get('tier', 'premium'),
                is_internal=data.get('isInternal', False)
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(data, indent=2),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'API key criada com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao criar API key: {e}')
            raise


@when('eu tento criar a API key')
@allure.story('API Keys - Create Error')
def tentar_criar_api_key(bdd_context, email_service_client):
    """
    Tentar criar uma API Key (pode gerar erro).

    Args:
        bdd_context: Contexto BDD (deve conter api_key_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Tentar criar API key'):
        try:
            data = bdd_context.api_key_data

            logger.info(f'Tentando criar API key: {data.get("name")}')

            response_data = email_service_client.create_api_key(
                name=data.get('name'),
                expiration_at=data.get('expirationAt'),
                tier=data.get('tier', 'premium'),
                is_internal=data.get('isInternal', False)
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'API key criada com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Erro esperado ao criar API key: {e}')


@when('eu busco a API key pelo ID')
@allure.story('API Keys - Get by ID')
def buscar_api_key_por_id(bdd_context, email_service_client):
    """
    Buscar uma API Key pelo ID.

    Args:
        bdd_context: Contexto BDD (deve conter api_key_id)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Buscar API key pelo ID'):
        try:
            api_key_id = bdd_context.api_key_id

            logger.info(f'Buscando API key com ID: {api_key_id}')

            response_data = email_service_client.get_api_key(api_key_id)

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                api_key_id,
                name='API Key ID',
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'API key encontrada com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao buscar API key: {e}')
            raise


@when(parsers.parse('eu tento buscar a API key com ID "{api_key_id}"'))
@allure.story('API Keys - Get by ID Error')
def tentar_buscar_api_key_com_id(bdd_context, email_service_client, api_key_id):
    """
    Tentar buscar uma API Key com ID específico (pode gerar erro).

    Args:
        bdd_context: Contexto BDD
        email_service_client: Cliente do Email Service
        api_key_id: ID da API Key a buscar
    """
    with allure.step(f'Tentar buscar API key com ID "{api_key_id}"'):
        try:
            logger.info(f'Tentando buscar API key com ID: {api_key_id}')

            response_data = email_service_client.get_api_key(api_key_id)

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'API key encontrada com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Erro esperado ao buscar API key: {e}')


@when('eu atualizo a API key')
@allure.story('API Keys - Update')
def atualizar_api_key(bdd_context, email_service_client):
    """
    Atualizar uma API Key existente.

    Args:
        bdd_context: Contexto BDD (deve conter api_key_id e api_key_updated_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Atualizar API key'):
        try:
            api_key_id = bdd_context.api_key_id
            data = bdd_context.api_key_updated_data

            logger.info(f'Atualizando API key ID: {api_key_id}')

            response_data = email_service_client.update_api_key(
                api_key_id,
                name=data.get('name'),
                is_active=data.get('isActive'),
                expiration_at=data.get('expirationAt'),
                tier=data.get('tier')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                api_key_id,
                name='API Key ID',
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(data, indent=2),
                name='Update Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'API key atualizada com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao atualizar API key: {e}')
            raise


@when('eu deleto a API key')
@allure.story('API Keys - Delete')
def deletar_api_key(bdd_context, email_service_client):
    """
    Deletar (soft delete) uma API Key.

    Args:
        bdd_context: Contexto BDD (deve conter api_key_id)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Deletar API key'):
        try:
            api_key_id = bdd_context.api_key_id

            logger.info(f'Deletando API key ID: {api_key_id}')

            response_data = email_service_client.delete_api_key(api_key_id)

            bdd_context.response_data = response_data
            bdd_context.status_code = 204

            allure.attach(
                api_key_id,
                name='API Key ID',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'API key deletada com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao deletar API key: {e}')
            raise


@when('eu tento listar as API keys')
@allure.story('API Keys - List Error')
def tentar_listar_api_keys(bdd_context, email_service_client):
    """
    Tentar listar API Keys (pode gerar erro).

    Args:
        bdd_context: Contexto BDD
        email_service_client: Cliente do Email Service
    """
    with allure.step('Tentar listar API keys'):
        try:
            logger.info(f'Tentando listar API keys')

            response_data = email_service_client.list_api_keys()

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'API keys listadas com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Erro esperado ao listar API keys: {e}')


# ============================================================================
# TEMPLATES - ACTIONS
# ============================================================================

@when(parsers.parse('eu listo os templates com os parâmetros:\n{params_table}'))
@allure.story('Templates - List')
def listar_templates_com_parametros(bdd_context, email_service_client, params_table):
    """
    Listar Templates com parâmetros de paginação e ordenação.

    Args:
        bdd_context: Contexto BDD
        email_service_client: Cliente do Email Service
        params_table: Tabela com parâmetros (page, limit, sort)
    """
    with allure.step('Listar templates com parâmetros'):
        try:
            params = _parse_params_table(params_table)

            logger.info(f'Listando templates com parâmetros: {params}')

            response_data = email_service_client.list_templates(
                page=params.get('page', 1),
                limit=params.get('limit', 10),
                sort=params.get('sort'),
                filters=params.get('filters')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(params, indent=2),
                name='Request Params',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Templates listados com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao listar templates: {e}')
            raise


@when(parsers.parse('eu listo os templates filtrando por tipo "{template_type}"'))
@allure.story('Templates - Filter')
def listar_templates_por_tipo(bdd_context, email_service_client, template_type):
    """
    Listar Templates filtrando por tipo.

    Args:
        bdd_context: Contexto BDD
        email_service_client: Cliente do Email Service
        template_type: Tipo de template (email, sms)
    """
    with allure.step(f'Listar templates filtrando por tipo "{template_type}"'):
        try:
            logger.info(f'Listando templates com tipo: {template_type}')

            response_data = email_service_client.list_templates(
                filters={'type': template_type}
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                template_type,
                name='Template Type',
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Templates filtrados com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao listar templates filtrados: {e}')
            raise


@when('eu crio um novo template')
@allure.story('Templates - Create')
def criar_template(bdd_context, email_service_client):
    """
    Criar um novo Template.

    Args:
        bdd_context: Contexto BDD (deve conter template_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Criar novo template'):
        try:
            data = bdd_context.template_data

            logger.info(f'Criando template: {data.get("name")}')

            response_data = email_service_client.create_template(
                type=data['type'],
                name=data['name'],
                subject=data.get('subject'),
                body=data.get('body'),
                html=data.get('html'),
                description=data.get('description')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(data, indent=2),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Template criado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao criar template: {e}')
            raise


@when('eu tento criar o template')
@allure.story('Templates - Create Error')
def tentar_criar_template(bdd_context, email_service_client):
    """
    Tentar criar um Template (pode gerar erro).

    Args:
        bdd_context: Contexto BDD (deve conter template_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Tentar criar template'):
        try:
            data = bdd_context.template_data

            logger.info(f'Tentando criar template: {data.get("name")}')

            response_data = email_service_client.create_template(
                type=data.get('type'),
                name=data.get('name'),
                subject=data.get('subject'),
                body=data.get('body'),
                html=data.get('html'),
                description=data.get('description')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Template criado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Erro esperado ao criar template: {e}')


@when('eu busco o template pelo ID')
@allure.story('Templates - Get by ID')
def buscar_template_por_id(bdd_context, email_service_client):
    """
    Buscar um Template pelo ID.

    Args:
        bdd_context: Contexto BDD (deve conter template_id)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Buscar template pelo ID'):
        try:
            template_id = bdd_context.template_id

            logger.info(f'Buscando template com ID: {template_id}')

            response_data = email_service_client.get_template(template_id)

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                template_id,
                name='Template ID',
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Template encontrado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao buscar template: {e}')
            raise


@when('eu atualizo o template')
@allure.story('Templates - Update')
def atualizar_template(bdd_context, email_service_client):
    """
    Atualizar um Template existente.

    Args:
        bdd_context: Contexto BDD (deve conter template_id e template_updated_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Atualizar template'):
        try:
            template_id = bdd_context.template_id
            data = bdd_context.template_updated_data

            logger.info(f'Atualizando template ID: {template_id}')

            response_data = email_service_client.update_template(
                template_id,
                name=data.get('name'),
                subject=data.get('subject'),
                body=data.get('body'),
                html=data.get('html'),
                description=data.get('description'),
                is_active=data.get('isActive')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                template_id,
                name='Template ID',
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(data, indent=2),
                name='Update Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Template atualizado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao atualizar template: {e}')
            raise


@when('eu deleto o template')
@allure.story('Templates - Delete')
def deletar_template(bdd_context, email_service_client):
    """
    Deletar (soft delete) um Template.

    Args:
        bdd_context: Contexto BDD (deve conter template_id)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Deletar template'):
        try:
            template_id = bdd_context.template_id

            logger.info(f'Deletando template ID: {template_id}')

            response_data = email_service_client.delete_template(template_id)

            bdd_context.response_data = response_data
            bdd_context.status_code = 204

            allure.attach(
                template_id,
                name='Template ID',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Template deletado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao deletar template: {e}')
            raise


# ============================================================================
# EMAIL SENDING - ACTIONS
# ============================================================================

@when('eu envio o email')
@allure.story('Email Sending - Send')
def enviar_email(bdd_context, email_service_client):
    """
    Enviar um email de forma síncrona.

    Args:
        bdd_context: Contexto BDD (deve conter email_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Enviar email'):
        try:
            data = bdd_context.email_data

            logger.info(f'Enviando email para: {data.get("to")}')

            response_data = email_service_client.send_email(
                to=data.get('to'),
                cc=data.get('cc'),
                bcc=data.get('bcc'),
                subject=data.get('subject'),
                body=data.get('body'),
                html=data.get('html'),
                attachments=data.get('attachments')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email enviado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao enviar email: {e}')
            raise


@when('eu envio um email simples')
@allure.story('Email Sending - Simple Email')
def enviar_email_simples(bdd_context, email_service_client):
    """
    Enviar um email simples (texto).

    Args:
        bdd_context: Contexto BDD (deve conter email_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Enviar email simples'):
        try:
            data = bdd_context.email_data

            logger.info(f'Enviando email simples para: {data.get("to")}')

            response_data = email_service_client.send_email(
                to=data.get('to'),
                subject=data.get('subject'),
                body=data.get('body')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email simples enviado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao enviar email simples: {e}')
            raise


@when('eu envio um email HTML')
@allure.story('Email Sending - HTML Email')
def enviar_email_html(bdd_context, email_service_client):
    """
    Enviar um email em formato HTML.

    Args:
        bdd_context: Contexto BDD (deve conter email_html_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Enviar email HTML'):
        try:
            data = bdd_context.email_html_data

            logger.info(f'Enviando email HTML para: {data.get("to")}')

            response_data = email_service_client.send_email(
                to=data.get('to'),
                cc=data.get('cc'),
                bcc=data.get('bcc'),
                subject=data.get('subject'),
                html=data.get('html')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email HTML enviado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao enviar email HTML: {e}')
            raise


@when('eu envio um email com template')
@allure.story('Email Sending - Template Email')
def enviar_email_com_template(bdd_context, email_service_client):
    """
    Enviar um email usando template.

    Args:
        bdd_context: Contexto BDD (deve conter email_template_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Enviar email com template'):
        try:
            data = bdd_context.email_template_data

            logger.info(f'Enviando email com template para: {data.get("to")}')

            response_data = email_service_client.send_email_with_template(
                to=data.get('to'),
                template_id=data.get('templateId'),
                variables=data.get('variables')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email com template enviado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao enviar email com template: {e}')
            raise


@when('eu envio um email com anexos')
@allure.story('Email Sending - Email with Attachments')
def enviar_email_com_anexos(bdd_context, email_service_client):
    """
    Enviar um email com anexos.

    Args:
        bdd_context: Contexto BDD (deve conter email_attachment_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Enviar email com anexos'):
        try:
            data = bdd_context.email_attachment_data

            logger.info(f'Enviando email com anexos para: {data.get("to")}')

            response_data = email_service_client.send_email(
                to=data.get('to'),
                subject=data.get('subject'),
                body=data.get('body'),
                attachments=data.get('attachments')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email com anexos enviado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao enviar email com anexos: {e}')
            raise


@when('eu tento enviar o email')
@allure.story('Email Sending - Send Error')
def tentar_enviar_email(bdd_context, email_service_client):
    """
    Tentar enviar um email (pode gerar erro).

    Args:
        bdd_context: Contexto BDD (deve conter email_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Tentar enviar email'):
        try:
            data = bdd_context.email_data

            logger.info(f'Tentando enviar email para: {data.get("to")}')

            response_data = email_service_client.send_email(
                to=data.get('to'),
                subject=data.get('subject'),
                body=data.get('body')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email enviado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Erro esperado ao enviar email: {e}')


@when('eu envio um email de forma síncrona')
@allure.story('Email Sending - Synchronous Send')
def enviar_email_sincronamente(bdd_context, email_service_client):
    """
    Enviar um email de forma síncrona.

    Args:
        bdd_context: Contexto BDD (deve conter email_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Enviar email de forma síncrona'):
        try:
            data = bdd_context.email_data

            logger.info(f'Enviando email de forma síncrona para: {data.get("to")}')

            response_data = email_service_client.send_email(
                to=data.get('to'),
                cc=data.get('cc'),
                bcc=data.get('bcc'),
                subject=data.get('subject'),
                body=data.get('body'),
                html=data.get('html'),
                attachments=data.get('attachments')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email enviado de forma síncrona com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao enviar email de forma síncrona: {e}')
            raise


@when('eu tento enviar o email usando template')
@allure.story('Email Sending - Template Send Error')
def tentar_enviar_email_com_template(bdd_context, email_service_client):
    """
    Tentar enviar um email com template (pode gerar erro).

    Args:
        bdd_context: Contexto BDD (deve conter email_template_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Tentar enviar email com template'):
        try:
            data = bdd_context.email_template_data

            logger.info(f'Tentando enviar email com template para: {data.get("to")}')

            response_data = email_service_client.send_email_with_template(
                to=data.get('to'),
                template_id=data.get('templateId'),
                variables=data.get('variables')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email com template enviado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Erro esperado ao enviar email com template: {e}')


# ============================================================================
# EMAIL QUEUE - ACTIONS
# ============================================================================

@when('eu adiciono o email na fila')
@allure.story('Email Queue - Add to Queue')
def adicionar_email_na_fila(bdd_context, email_service_client):
    """
    Adicionar um email na fila para processamento assíncrono.

    Args:
        bdd_context: Contexto BDD (deve conter email_queue_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Adicionar email na fila'):
        try:
            data = bdd_context.email_queue_data

            logger.info(f'Adicionando email na fila para: {data.get("to")}')

            response_data = email_service_client.queue_email(
                to=data.get('to'),
                subject=data.get('subject'),
                text_content=data.get('textContent'),
                html_content=data.get('htmlContent'),
                priority=data.get('priority', 'medium'),
                track_opens=data.get('trackOpens', False),
                track_clicks=data.get('trackClicks', False)
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email adicionado na fila com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao adicionar email na fila: {e}')
            raise


@when('eu adiciono um lote de emails na fila')
@allure.story('Email Queue - Bulk Queue')
def adicionar_lote_emails_fila(bdd_context, email_service_client):
    """
    Adicionar um lote de emails na fila para processamento em massa.

    Args:
        bdd_context: Contexto BDD (deve conter email_bulk_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Adicionar lote de emails na fila'):
        try:
            data = bdd_context.email_bulk_data

            logger.info(f'Adicionando lote de emails na fila')

            response_data = email_service_client.queue_emails_bulk(
                template_id=data.get('templateId'),
                recipients=data.get('recipients'),
                batch_size=data.get('batchSize', 100),
                batch_delay=data.get('batchDelay', 5),
                priority=data.get('priority', 'medium')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Lote de emails adicionado na fila com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao adicionar lote de emails na fila: {e}')
            raise


@when('eu agendar o email')
@allure.story('Email Queue - Schedule Email')
def agendar_email(bdd_context, email_service_client):
    """
    Agendar um email para envio futuro.

    Args:
        bdd_context: Contexto BDD (deve conter email_scheduled_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Agendar email para envio futuro'):
        try:
            data = bdd_context.email_scheduled_data

            logger.info(f'Agendando email para: {data.get("to")}')

            response_data = email_service_client.schedule_email(
                to=data.get('to'),
                subject=data.get('subject'),
                template_id=data.get('templateId'),
                scheduled_for=data.get('scheduledFor'),
                timezone=data.get('timezone'),
                priority=data.get('priority', 'medium')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(data, indent=2, default=str),
                name='Request Data',
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email agendado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao agendar email: {e}')
            raise


@when('eu consulto o status do email pelo trackingId')
@allure.story('Email Queue - Check Status')
def consultar_status_email(bdd_context, email_service_client):
    """
    Consultar o status de um email na fila.

    Args:
        bdd_context: Contexto BDD (deve conter tracking_id)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Consultar status do email'):
        try:
            tracking_id = bdd_context.tracking_id

            logger.info(f'Consultando status do email: {tracking_id}')

            response_data = email_service_client.get_email_status(tracking_id)

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                tracking_id,
                name='Tracking ID',
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Status do email consultado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao consultar status do email: {e}')
            raise


@when('eu consulto o status do envio em massa')
@allure.story('Email Queue - Bulk Status')
def consultar_status_envio_massa(bdd_context, email_service_client):
    """
    Consultar o status de um envio em massa.

    Args:
        bdd_context: Contexto BDD (deve conter batch_id)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Consultar status do envio em massa'):
        try:
            batch_id = bdd_context.batch_id

            logger.info(f'Consultando status do lote: {batch_id}')

            response_data = email_service_client.get_batch_status(batch_id)

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                batch_id,
                name='Batch ID',
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Status do lote consultado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao consultar status do lote: {e}')
            raise


@when('eu cancelo o email agendado')
@allure.story('Email Queue - Cancel Scheduled')
def cancelar_email_agendado(bdd_context, email_service_client):
    """
    Cancelar um email agendado.

    Args:
        bdd_context: Contexto BDD (deve conter schedule_id)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Cancelar email agendado'):
        try:
            schedule_id = bdd_context.schedule_id

            logger.info(f'Cancelando email agendado: {schedule_id}')

            response_data = email_service_client.cancel_scheduled_email(schedule_id)

            bdd_context.response_data = response_data
            bdd_context.status_code = 200

            allure.attach(
                schedule_id,
                name='Schedule ID',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Email agendado cancelado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.error(f'Erro ao cancelar email agendado: {e}')
            raise


@when('eu tento adicionar na fila')
@allure.story('Email Queue - Queue Error')
def tentar_adicionar_fila(bdd_context, email_service_client):
    """
    Tentar adicionar email na fila (pode gerar erro).

    Args:
        bdd_context: Contexto BDD
        email_service_client: Cliente do Email Service
    """
    with allure.step('Tentar adicionar email na fila'):
        try:
            data = bdd_context.email_queue_data

            logger.info(f'Tentando adicionar email na fila para: {data.get("to")}')

            response_data = email_service_client.queue_email(
                to=data.get('to'),
                subject=data.get('subject'),
                text_content=data.get('textContent')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email adicionado na fila com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Erro esperado ao adicionar email na fila: {e}')


@when('eu tento agendar o email')
@allure.story('Email Queue - Schedule Error')
def tentar_agendar_email(bdd_context, email_service_client):
    """
    Tentar agendar um email (pode gerar erro).

    Args:
        bdd_context: Contexto BDD (deve conter email_scheduled_data)
        email_service_client: Cliente do Email Service
    """
    with allure.step('Tentar agendar email'):
        try:
            data = bdd_context.email_scheduled_data

            logger.info(f'Tentando agendar email para: {data.get("to")}')

            response_data = email_service_client.schedule_email(
                to=data.get('to'),
                subject=data.get('subject'),
                template_id=data.get('templateId'),
                scheduled_for=data.get('scheduledFor'),
                timezone=data.get('timezone')
            )

            bdd_context.response_data = response_data
            bdd_context.status_code = 201

            allure.attach(
                json.dumps(response_data, indent=2, default=str),
                name='Response Data',
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(f'Email agendado com sucesso')

        except Exception as e:
            bdd_context.error = str(e)
            bdd_context.status_code = getattr(e, 'status_code', 500)

            allure.attach(
                str(e),
                name='Error Details',
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f'Erro esperado ao agendar email: {e}')
