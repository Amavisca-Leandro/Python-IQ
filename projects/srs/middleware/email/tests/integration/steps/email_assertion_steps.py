"""
Step definitions de asserções para testes BDD do Email Service.

Este módulo fornece steps reutilizáveis para validações de respostas da API
de API Keys do serviço de email. Todas as asserções são envolvidas com steps
do Allure para relatórios detalhados.

Steps:
- Então o status code deve ser {status_code}
- Então o status code deve ser {status_code1} ou {status_code2}
- Então a resposta deve conter uma lista de API keys
- Então a resposta deve conter o campo "{field}"
- Então o campo "{field}" deve ser "{value}"
- Então o campo "{field}" deve ser verdadeiro
- Então o campo "{field}" deve corresponder ao ID salvo
- Então a lista deve ter no máximo {max_count} itens
- Então cada API key deve conter os campos obrigatórios
- Então devo salvar o "{field}" retornado como "{context_var}"
- Então a API key deve ser marcada como inativa
- Então todas as API keys retornadas devem ter isActive igual a {value}
- Então a mensagem de erro deve conter "{text}"
- Então que existe uma API key com ID salvo
"""

import allure
import logging
from pytest_bdd import then, given, parsers
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Allure feature and story decorators for this module
allure.feature("Email Service - API Keys")
allure.story("Response Assertions")


# ============================================================================
# STATUS CODE ASSERTIONS
# ============================================================================

@then(parsers.parse("o status code deve ser {status_code:d}"))
@allure.story("Status Code Validation")
def verificar_status_code(bdd_context, status_code: int):
    """
    Verifica se o status code da resposta corresponde ao esperado.

    Este step valida que o status HTTP retornado pela API é exatamente
    o valor especificado. É envolvido com um step do Allure para
    relatórios detalhados.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        status_code: Código HTTP esperado (ex: 200, 201, 404)

    Raises:
        AssertionError: Se o status code não corresponder
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então o status code deve ser 200
        Então o status code deve ser 201
        Então o status code deve ser 404
    """
    with allure.step(f"Verificar que o status code é {status_code}"):
        assert hasattr(bdd_context, 'status_code'), \
            "Nenhum status code encontrado no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        actual_status = bdd_context.status_code

        # Anexar informações ao relatório Allure
        allure.attach(
            str(actual_status),
            name="Status Code Atual",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            str(status_code),
            name="Status Code Esperado",
            attachment_type=allure.attachment_type.TEXT
        )

        assert actual_status == status_code, \
            f"Esperado status code {status_code}, mas recebido {actual_status}"

        logger.info(f"Validação de status code passou: {status_code}")


@then(parsers.parse("o status code deve ser {status_code1:d} ou {status_code2:d}"))
@allure.story("Status Code Validation")
def verificar_status_code_multiplo(bdd_context, status_code1: int, status_code2: int):
    """
    Verifica se o status code está entre dois valores possíveis.

    Este step valida que o status HTTP é um de dois valores aceitos.
    Útil para operações que podem retornar múltiplos códigos de sucesso.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        status_code1: Primeiro código HTTP aceito
        status_code2: Segundo código HTTP aceito

    Raises:
        AssertionError: Se o status code não for um dos esperados
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então o status code deve ser 204 ou 200
        Então o status code deve ser 401 ou 403
    """
    with allure.step(f"Verificar que o status code é {status_code1} ou {status_code2}"):
        assert hasattr(bdd_context, 'status_code'), \
            "Nenhum status code encontrado no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        actual_status = bdd_context.status_code

        # Anexar informações ao relatório Allure
        allure.attach(
            str(actual_status),
            name="Status Code Atual",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            f"{status_code1} ou {status_code2}",
            name="Status Codes Esperados",
            attachment_type=allure.attachment_type.TEXT
        )

        assert actual_status in (status_code1, status_code2), \
            f"Esperado status code {status_code1} ou {status_code2}, mas recebido {actual_status}"

        logger.info(f"Validação de status code passou: {actual_status} (aceitável)")


# ============================================================================
# RESPONSE TYPE ASSERTIONS
# ============================================================================

@then("a resposta deve conter uma lista de API keys")
@allure.story("Response Type Validation")
def verificar_lista_api_keys(bdd_context):
    """
    Verifica se a resposta contém uma lista de API keys.

    Este step valida que a resposta JSON é uma lista e contém
    estruturas de API key. É usado para validar endpoints que
    retornam múltiplas API keys.

    Args:
        bdd_context: Contexto BDD contendo a resposta

    Raises:
        AssertionError: Se a resposta não for uma lista
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então a resposta deve conter uma lista de API keys
    """
    with allure.step("Verificar que a resposta contém uma lista de API keys"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        assert isinstance(data, list), \
            f"Esperado que a resposta seja uma lista, mas recebida {type(data).__name__}"

        # Anexar detalhes ao relatório Allure
        allure.attach(
            str(len(data)),
            name="Número de API Keys",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Resposta contém uma lista com {len(data)} API keys")


# ============================================================================
# FIELD ASSERTIONS
# ============================================================================

@then(parsers.parse('a resposta deve conter o campo "{field}"'))
@allure.story("Field Validation")
def verificar_campo_existe(bdd_context, field: str):
    """
    Verifica se a resposta contém um campo específico.

    Este step valida que um campo (chave) existe no dicionário
    de resposta JSON. Não valida o valor, apenas a presença do campo.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        field: Nome do campo a verificar

    Raises:
        AssertionError: Se o campo não existir na resposta
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então a resposta deve conter o campo "id"
        Então a resposta deve conter o campo "value"
    """
    with allure.step(f"Verificar que a resposta contém o campo '{field}'"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        assert isinstance(data, dict), \
            f"Não é possível verificar campo em {type(data).__name__}. A resposta deve ser um dicionário."

        assert field in data, \
            f"Campo '{field}' não encontrado na resposta. Campos disponíveis: {list(data.keys())}"

        # Anexar informações ao relatório Allure
        allure.attach(
            field,
            name="Nome do Campo",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            str(data[field]),
            name="Valor do Campo",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Campo '{field}' existe na resposta com valor: {data[field]}")


@then(parsers.parse('o campo "{field}" deve ser "{value}"'))
@allure.story("Field Validation")
def verificar_valor_campo(bdd_context, field: str, value: str):
    """
    Verifica se um campo da resposta tem um valor específico.

    Este step valida que um campo no JSON de resposta tem o valor
    esperado. A comparação é feita como strings para lidar com
    diferentes tipos de dados.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        field: Nome do campo a verificar
        value: Valor esperado (como string)

    Raises:
        AssertionError: Se o valor do campo não corresponder
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então o campo "name" deve ser "My API Key"
        Então o campo "tier" deve ser "premium"
    """
    with allure.step(f"Verificar que o campo '{field}' é '{value}'"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        assert isinstance(data, dict), \
            f"Não é possível verificar campo em {type(data).__name__}. A resposta deve ser um dicionário."

        assert field in data, \
            f"Campo '{field}' não encontrado na resposta. Campos disponíveis: {list(data.keys())}"

        actual_value = str(data[field])

        # Anexar detalhes de comparação ao relatório Allure
        allure.attach(
            actual_value,
            name="Valor Atual",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            value,
            name="Valor Esperado",
            attachment_type=allure.attachment_type.TEXT
        )

        assert actual_value == value, \
            f"Esperado que o campo '{field}' seja '{value}', mas recebido '{actual_value}'"

        logger.info(f"Campo '{field}' tem o valor esperado: {value}")


@then(parsers.parse('o campo "{field}" deve ser verdadeiro'))
@allure.story("Field Validation")
def verificar_campo_verdadeiro(bdd_context, field: str):
    """
    Verifica se um campo da resposta é verdadeiro (true).

    Este step valida que um campo booleano tem valor true.
    Útil para validar flags de status como isActive.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        field: Nome do campo booleano

    Raises:
        AssertionError: Se o campo não for true
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então o campo "isActive" deve ser verdadeiro
    """
    with allure.step(f"Verificar que o campo '{field}' é verdadeiro"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        assert isinstance(data, dict), \
            f"Não é possível verificar campo em {type(data).__name__}. A resposta deve ser um dicionário."

        assert field in data, \
            f"Campo '{field}' não encontrado na resposta. Campos disponíveis: {list(data.keys())}"

        actual_value = data[field]

        # Anexar detalhes ao relatório Allure
        allure.attach(
            str(actual_value),
            name="Valor do Campo",
            attachment_type=allure.attachment_type.TEXT
        )

        assert actual_value is True, \
            f"Esperado que o campo '{field}' seja verdadeiro (true), mas recebido {actual_value} ({type(actual_value).__name__})"

        logger.info(f"Campo '{field}' é verdadeiro como esperado")


@then(parsers.parse('o campo "{field}" deve corresponder ao ID salvo'))
@allure.story("Field Validation")
def verificar_campo_corresponde_id_salvo(bdd_context, field: str):
    """
    Verifica se um campo corresponde ao ID de API key previamente salvo.

    Este step compara o valor de um campo com o ID salvo no contexto
    durante um passo anterior. É útil para validar que o ID retornado
    corresponde ao ID solicitado.

    Args:
        bdd_context: Contexto BDD contendo a resposta e ID salvo
        field: Nome do campo a comparar

    Raises:
        AssertionError: Se o campo não corresponder ao ID salvo
        AttributeError: Se nenhuma resposta estiver no contexto ou ID não estiver salvo

    Exemplo no arquivo de feature:
        Então o campo "id" deve corresponder ao ID salvo
    """
    with allure.step(f"Verificar que o campo '{field}' corresponde ao ID salvo"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        assert hasattr(bdd_context, 'api_key_id'), \
            "Nenhum ID de API key salvo no contexto. Certifique-se de que foi salvo em um passo anterior."

        data = bdd_context.response_data

        assert isinstance(data, dict), \
            f"Não é possível verificar campo em {type(data).__name__}. A resposta deve ser um dicionário."

        assert field in data, \
            f"Campo '{field}' não encontrado na resposta. Campos disponíveis: {list(data.keys())}"

        actual_value = str(data[field])
        saved_id = str(bdd_context.api_key_id)

        # Anexar detalhes de comparação ao relatório Allure
        allure.attach(
            actual_value,
            name="ID na Resposta",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            saved_id,
            name="ID Salvo",
            attachment_type=allure.attachment_type.TEXT
        )

        assert actual_value == saved_id, \
            f"Esperado que o campo '{field}' seja '{saved_id}' (ID salvo), mas recebido '{actual_value}'"

        logger.info(f"Campo '{field}' corresponde ao ID salvo: {saved_id}")


# ============================================================================
# LIST ASSERTIONS
# ============================================================================

@then(parsers.parse("a lista deve ter no máximo {max_count:d} itens"))
@allure.story("List Validation")
def verificar_lista_tamanho_maximo(bdd_context, max_count: int):
    """
    Verifica se a lista de resposta não excede o número máximo de itens.

    Este step valida que a lista retornada tem no máximo o número
    especificado de itens. É útil para validar paginação.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        max_count: Número máximo de itens permitidos

    Raises:
        AssertionError: Se a lista tiver mais itens que o máximo
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então a lista deve ter no máximo 10 itens
    """
    with allure.step(f"Verificar que a lista tem no máximo {max_count} itens"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        assert isinstance(data, list), \
            f"Não é possível verificar tamanho em {type(data).__name__}. A resposta deve ser uma lista."

        actual_count = len(data)

        # Anexar detalhes ao relatório Allure
        allure.attach(
            str(actual_count),
            name="Número de Itens na Lista",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            str(max_count),
            name="Número Máximo Permitido",
            attachment_type=allure.attachment_type.TEXT
        )

        assert actual_count <= max_count, \
            f"Esperado no máximo {max_count} itens, mas recebida lista com {actual_count} itens"

        logger.info(f"Lista tem {actual_count} itens (máximo {max_count})")


@then(parsers.parse("cada API key deve conter os campos obrigatórios:\n{fields_table}"))
@allure.story("Field Validation")
def verificar_campos_obrigatorios_api_key(bdd_context, fields_table: str):
    """
    Verifica se cada API key na lista contém todos os campos obrigatórios.

    Este step valida que todos os itens de uma lista de API keys possuem
    os campos especificados. Cada campo é verificado em cada API key.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        fields_table: Tabela Gherkin com os campos obrigatórios

    Raises:
        AssertionError: Se alguma API key estiver faltando um campo obrigatório
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então cada API key deve conter os campos obrigatórios:
            | campo        |
            | id           |
            | name         |
            | value        |
            | expirationAt |
            | tier         |
            | isActive     |
    """
    with allure.step("Verificar que cada API key contém os campos obrigatórios"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        assert isinstance(data, list), \
            f"Não é possível verificar itens em {type(data).__name__}. A resposta deve ser uma lista."

        assert len(data) > 0, \
            "Não é possível verificar campos em lista vazia"

        # Parse campos obrigatórios da tabela
        required_fields = _parse_fields_table(fields_table)

        # Verificar cada API key
        missing_fields_by_index = {}
        for index, api_key in enumerate(data):
            if not isinstance(api_key, dict):
                raise AssertionError(
                    f"API key no índice {index} não é um dicionário. "
                    f"Recebido {type(api_key).__name__} ao invés."
                )

            missing_fields = [field for field in required_fields if field not in api_key]
            if missing_fields:
                missing_fields_by_index[index] = missing_fields

        # Anexar detalhes ao relatório Allure
        allure.attach(
            str(len(data)),
            name="Total de API Keys Verificadas",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            str(required_fields),
            name="Campos Obrigatórios",
            attachment_type=allure.attachment_type.JSON
        )

        if missing_fields_by_index:
            allure.attach(
                str(missing_fields_by_index),
                name="Campos Faltantes por Índice",
                attachment_type=allure.attachment_type.JSON
            )

            raise AssertionError(
                f"Campos obrigatórios faltando em {len(missing_fields_by_index)} API keys: {missing_fields_by_index}"
            )

        logger.info(f"Todas as {len(data)} API keys contêm os campos obrigatórios")


# ============================================================================
# CONTEXT DATA STORAGE ASSERTIONS
# ============================================================================

@then(parsers.parse('devo salvar o "{field}" retornado como "{context_var}"'))
@allure.story("Context Storage")
def salvar_campo_no_contexto(bdd_context, field: str, context_var: str):
    """
    Salva um campo da resposta no contexto BDD para uso posterior.

    Este step extrai um valor do JSON de resposta e o armazena no
    contexto BDD para que seja usado em passos subsequentes.

    Args:
        bdd_context: Contexto BDD para armazenar dados
        field: Nome do campo a extrair da resposta
        context_var: Nome da variável no contexto para armazenar

    Raises:
        AssertionError: Se o campo não existir na resposta
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então devo salvar o "id" retornado como "api_key_id"
        Então devo salvar o "value" retornado como "api_key_value"
    """
    with allure.step(f"Salvar o campo '{field}' como '{context_var}'"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        assert isinstance(data, dict), \
            f"Não é possível extrair campo de {type(data).__name__}. A resposta deve ser um dicionário."

        assert field in data, \
            f"Campo '{field}' não encontrado na resposta. Campos disponíveis: {list(data.keys())}"

        value = data[field]

        # Armazenar no contexto BDD
        setattr(bdd_context, context_var, value)

        # Anexar ao relatório Allure
        allure.attach(
            str(value),
            name=f"{context_var} (salvo de '{field}')",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Campo '{field}' salvo no contexto como '{context_var}': {value}")


# ============================================================================
# API KEY STATUS ASSERTIONS
# ============================================================================

@then("a API key deve ser marcada como inativa")
@allure.story("API Key Status Validation")
def verificar_api_key_inativa(bdd_context, email_service_client):
    """
    Verifica que a API key foi marcada como inativa após deleção.

    Este step valida que após uma operação de delete (soft delete),
    a API key tem o status isActive = false.

    Args:
        bdd_context: Contexto BDD contendo o ID da API key
        email_service_client: Cliente do Email Service

    Raises:
        AssertionError: Se a API key não estiver marcada como inativa
        AttributeError: Se o ID da API key não estiver no contexto

    Exemplo no arquivo de feature:
        Então a API key deve ser marcada como inativa
    """
    with allure.step("Verificar que a API key está marcada como inativa"):
        assert hasattr(bdd_context, 'api_key_id'), \
            "Nenhum ID de API key salvo no contexto. Certifique-se de que foi salvo em um passo anterior."

        api_key_id = bdd_context.api_key_id

        # Buscar a API key pelo ID para verificar seu status
        try:
            response_data = email_service_client.get_api_key(api_key_id)

            assert isinstance(response_data, dict), \
                f"Resposta deve ser um dicionário, recebido {type(response_data).__name__}"

            assert 'isActive' in response_data, \
                f"Campo 'isActive' não encontrado na resposta. Campos: {list(response_data.keys())}"

            is_active = response_data['isActive']

            # Anexar detalhes ao relatório Allure
            allure.attach(
                str(is_active),
                name="Status isActive",
                attachment_type=allure.attachment_type.TEXT
            )

            assert is_active is False, \
                f"Esperado que a API key seja inativa (isActive=false), mas recebido isActive={is_active}"

            logger.info(f"API key {api_key_id} está marcada como inativa")

        except Exception as e:
            raise AssertionError(f"Erro ao verificar status da API key: {str(e)}")


@then(parsers.parse("todas as API keys retornadas devem ter isActive igual a {value}"))
@allure.story("API Key Filter Validation")
def verificar_todas_api_keys_status(bdd_context, value: str):
    """
    Verifica que todas as API keys retornadas têm o mesmo status isActive.

    Este step valida que quando filtrando por status, todas as API keys
    retornadas têm o valor isActive especificado.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        value: Valor esperado de isActive ("true" ou "false" como string)

    Raises:
        AssertionError: Se alguma API key tiver status diferente
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então todas as API keys retornadas devem ter isActive igual a true
        Então todas as API keys retornadas devem ter isActive igual a false
    """
    with allure.step(f"Verificar que todas as API keys têm isActive = {value}"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        assert isinstance(data, list), \
            f"Não é possível verificar itens em {type(data).__name__}. A resposta deve ser uma lista."

        # Converter valor string para booleano
        expected_value = value.lower() == 'true'

        # Verificar cada API key
        mismatched_indices = []
        for index, api_key in enumerate(data):
            if not isinstance(api_key, dict):
                raise AssertionError(
                    f"API key no índice {index} não é um dicionário. "
                    f"Recebido {type(api_key).__name__} ao invés."
                )

            if 'isActive' not in api_key:
                raise AssertionError(
                    f"Campo 'isActive' não encontrado na API key no índice {index}"
                )

            actual_value = api_key['isActive']
            if actual_value != expected_value:
                mismatched_indices.append({
                    'index': index,
                    'id': api_key.get('id', 'unknown'),
                    'isActive': actual_value
                })

        # Anexar detalhes ao relatório Allure
        allure.attach(
            str(len(data)),
            name="Total de API Keys Verificadas",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            str(expected_value),
            name="Valor isActive Esperado",
            attachment_type=allure.attachment_type.TEXT
        )

        if mismatched_indices:
            allure.attach(
                str(mismatched_indices),
                name="API Keys com Status Diferente",
                attachment_type=allure.attachment_type.JSON
            )

            raise AssertionError(
                f"Esperado que todas as API keys tenham isActive={expected_value}, "
                f"mas encontradas {len(mismatched_indices)} com valor diferente"
            )

        logger.info(f"Todas as {len(data)} API keys têm isActive = {expected_value}")


# ============================================================================
# ERROR MESSAGE ASSERTIONS
# ============================================================================

@then(parsers.parse('a mensagem de erro deve conter "{text}"'))
@allure.story("Error Validation")
def verificar_mensagem_erro_contem(bdd_context, text: str):
    """
    Verifica que a mensagem de erro da resposta contém um texto específico.

    Este step valida que mensagens de erro ou validação contêm
    o texto esperado. É útil para validar mensagens de erro em
    testes negativos.

    Args:
        bdd_context: Contexto BDD contendo a resposta
        text: Texto esperado na mensagem de erro

    Raises:
        AssertionError: Se o texto não estiver na mensagem de erro
        AttributeError: Se nenhuma resposta estiver no contexto

    Exemplo no arquivo de feature:
        Então a mensagem de erro deve conter "name is required"
        Então a mensagem de erro deve conter "not found"
    """
    with allure.step(f"Verificar que a mensagem de erro contém '{text}'"):
        assert hasattr(bdd_context, 'response_data'), \
            "Nenhuma resposta encontrada no contexto. Certifique-se de que um step de requisição foi executado primeiro."

        data = bdd_context.response_data

        # Buscar mensagem de erro em várias posições possíveis
        error_message = None
        if isinstance(data, dict):
            # Procurar em campos comuns de erro
            error_message = (
                data.get('message') or
                data.get('error') or
                data.get('detail') or
                data.get('msg') or
                data.get('errorMessage')
            )

        if error_message is None:
            error_message = str(data)

        error_message = str(error_message)

        # Anexar detalhes ao relatório Allure
        allure.attach(
            error_message,
            name="Mensagem de Erro Recebida",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            text,
            name="Texto Esperado",
            attachment_type=allure.attachment_type.TEXT
        )

        assert text.lower() in error_message.lower(), \
            f"Esperado que a mensagem de erro contenha '{text}', mas recebido: {error_message}"

        logger.info(f"Mensagem de erro contém o texto esperado: '{text}'")


# ============================================================================
# GIVEN STEPS (PREREQUISITE ASSERTIONS)
# ============================================================================

@given("que existe uma API key com ID salvo")
@allure.story("API Key Prerequisite")
def existir_api_key_com_id_salvo(bdd_context, email_service_client):
    """
    Garante que existe uma API key com ID salvo no contexto.

    Este step é usado como pré-condição para outros testes. Se um ID
    de API key já foi salvo no contexto, verifica que ainda existe.
    Se não existe, cria uma nova API key e salva o ID.

    Args:
        bdd_context: Contexto BDD
        email_service_client: Cliente do Email Service

    Raises:
        AssertionError: Se não conseguir criar ou encontrar uma API key

    Exemplo no arquivo de feature:
        Dado que existe uma API key com ID salvo
    """
    with allure.step("Garantir que existe uma API key com ID salvo"):
        # Verificar se já existe um ID salvo
        if hasattr(bdd_context, 'api_key_id'):
            api_key_id = bdd_context.api_key_id

            # Verificar se a API key ainda existe
            try:
                response_data = email_service_client.get_api_key(api_key_id)

                allure.attach(
                    api_key_id,
                    name="ID da API Key Existente",
                    attachment_type=allure.attachment_type.TEXT
                )

                logger.info(f"API key existente encontrada com ID: {api_key_id}")
                return
            except Exception:
                # API key não existe, criar uma nova
                logger.warning(f"API key com ID {api_key_id} não encontrada, criando nova")

        # Criar uma nova API key
        try:
            response_data = email_service_client.create_api_key(
                name="Test API Key for Prerequisites",
                expiration_at="2025-12-31T23:59:59Z",
                tier="premium",
                is_internal=False
            )

            # Salvar o ID no contexto
            api_key_id = response_data.get('id')
            assert api_key_id is not None, \
                "Campo 'id' não encontrado na resposta de criação de API key"

            bdd_context.api_key_id = api_key_id

            allure.attach(
                api_key_id,
                name="ID da API Key Criada",
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info(f"Nova API key criada com ID: {api_key_id}")

        except Exception as e:
            raise AssertionError(f"Erro ao criar API key para pré-condição: {str(e)}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _parse_fields_table(fields_table: str) -> List[str]:
    """
    Converte uma tabela Gherkin de campos em lista Python.

    Args:
        fields_table: String da tabela Gherkin

    Returns:
        Lista com os nomes dos campos
    """
    fields = []
    lines = fields_table.strip().split('\n')

    # Pular linha de cabeçalho
    for line in lines[1:]:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]

            if len(parts) >= 1:
                field = parts[0]
                fields.append(field)

    return fields
