"""
Testes BDD para Gerenciamento de API Keys.

Este módulo executa os cenários definidos em api_keys.feature.
"""

import pytest
from pytest_bdd import scenarios

# Import step definitions específicos do SRS Email Service
from .steps.email_common_steps import *  # noqa: F401, F403
from .steps.email_api_steps import *  # noqa: F401, F403
from .steps.email_assertion_steps import *  # noqa: F401, F403

# Carregar todos os cenários do arquivo .feature
scenarios('features/api_keys.feature')
