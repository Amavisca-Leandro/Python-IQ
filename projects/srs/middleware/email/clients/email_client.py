"""
Cliente para Email Service do SRS Middleware - Communication API.

Este módulo fornece um cliente HTTP completo para interagir com todos os
endpoints do serviço de comunicação (email, templates, API keys).
"""

import os
from typing import Dict, Any, Optional, List
from core.api.client import APIClient


class EmailServiceClient(APIClient):
    """
    Cliente para o Communication API do middleware SRS.

    Suporta:
    - Gerenciamento de API Keys
    - Gerenciamento de Templates
    - Envio direto de emails (síncrono)
    - Fila de emails (assíncrono, bulk, scheduled)

    Examples:
        >>> client = EmailServiceClient()
        >>> # Criar API Key
        >>> api_key = client.create_api_key("My Key", "2025-12-31T23:59:59Z")
        >>> # Enviar email
        >>> email = client.send_email(["user@example.com"], "Hello", "Test email")
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        retries: Optional[int] = None
    ):
        """
        Inicializa o cliente do Email Service.

        Args:
            base_url: URL base do serviço (default: EMAIL_SERVICE_URL do .env.srs)
            api_key: API Key para autenticação (default: EMAIL_SERVICE_API_KEY)
            timeout: Timeout em segundos (default: 30)
            retries: Número de tentativas (default: 3)
        """
        self.base_url = base_url or os.getenv("EMAIL_SERVICE_URL", "http://localhost:3000")
        self.api_key = api_key or os.getenv("EMAIL_SERVICE_API_KEY")
        timeout = timeout or int(os.getenv("EMAIL_SERVICE_TIMEOUT", "30"))
        retries = retries or int(os.getenv("EMAIL_SERVICE_RETRIES", "3"))

        super().__init__(
            base_url=self.base_url,
            timeout=timeout,
            retries=retries
        )

        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})

    # ==================== API KEYS ====================

    def list_api_keys(
        self,
        page: int = 1,
        limit: int = 10,
        sort: Optional[Dict[str, str]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Lista todas as API keys com paginação.

        Args:
            page: Número da página
            limit: Itens por página
            sort: Ordenação (ex: {"name": "asc"})
            filters: Filtros (ex: {"isActive": True})

        Returns:
            Lista paginada de API keys
        """
        params = {"page": page, "limit": limit}

        if sort:
            for key, value in sort.items():
                params[f"sort[{key}]"] = value

        if filters:
            for key, value in filters.items():
                params[f"filter[{key}]"] = value

        response = self.get("/api-keys", params=params)
        return response.json()

    def get_api_key(self, api_key_id: str) -> Dict[str, Any]:
        """Busca uma API key específica por ID."""
        response = self.get(f"/api-keys/{api_key_id}")
        return response.json()

    def create_api_key(
        self,
        name: str,
        expiration_at: str,
        tier: str = "premium",
        is_internal: bool = False
    ) -> Dict[str, Any]:
        """
        Cria uma nova API key.

        Args:
            name: Nome da API key
            expiration_at: Data de expiração (ISO 8601)
            tier: Tier (premium, basic, etc.)
            is_internal: Se é interna

        Returns:
            API key criada com ID e value
        """
        payload = {
            "name": name,
            "expirationAt": expiration_at,
            "tier": tier,
            "isInternal": is_internal
        }
        response = self.post("/api-keys", json=payload)
        return response.json()

    def update_api_key(
        self,
        api_key_id: str,
        name: Optional[str] = None,
        is_active: Optional[bool] = None,
        expiration_at: Optional[str] = None,
        tier: Optional[str] = None
    ) -> Dict[str, Any]:
        """Atualiza uma API key existente."""
        payload = {"id": api_key_id}

        if name is not None:
            payload["name"] = name
        if is_active is not None:
            payload["isActive"] = is_active
        if expiration_at is not None:
            payload["expirationAt"] = expiration_at
        if tier is not None:
            payload["tier"] = tier

        response = self.put(f"/api-keys/{api_key_id}", json=payload)
        return response.json()

    def delete_api_key(self, api_key_id: str) -> Dict[str, Any]:
        """Deleta (soft delete) uma API key."""
        payload = {"id": api_key_id}
        response = self.delete(f"/api-keys/{api_key_id}", json=payload)
        return response.json() if response.text else {}

    # ==================== TEMPLATES ====================

    def list_templates(
        self,
        page: int = 1,
        limit: int = 10,
        template_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lista todos os templates com paginação.

        Args:
            page: Número da página
            limit: Itens por página
            template_type: Filtrar por tipo (email, sms)

        Returns:
            Lista paginada de templates
        """
        params = {"page": page, "limit": limit}

        if template_type:
            params["filter[type]"] = template_type

        response = self.get("/templates", params=params)
        return response.json()

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Busca um template específico por ID."""
        response = self.get(f"/templates/{template_id}")
        return response.json()

    def create_template(
        self,
        template_type: str,
        name: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cria um novo template.

        Args:
            template_type: Tipo (email, sms)
            name: Nome do template
            subject: Assunto (pode conter {{variables}})
            body: Corpo em texto
            html: Corpo em HTML (opcional)
            description: Descrição

        Returns:
            Template criado com ID
        """
        payload = {
            "type": template_type,
            "name": name,
            "subject": subject,
            "body": body
        }

        if html:
            payload["html"] = html
        if description:
            payload["description"] = description

        response = self.post("/templates", json=payload)
        return response.json()

    def update_template(
        self,
        template_id: str,
        name: Optional[str] = None,
        subject: Optional[str] = None,
        body: Optional[str] = None,
        html: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Atualiza um template existente."""
        payload = {"id": template_id}

        if name is not None:
            payload["name"] = name
        if subject is not None:
            payload["subject"] = subject
        if body is not None:
            payload["body"] = body
        if html is not None:
            payload["html"] = html
        if description is not None:
            payload["description"] = description
        if is_active is not None:
            payload["isActive"] = is_active

        response = self.put(f"/templates/{template_id}", json=payload)
        return response.json()

    def delete_template(self, template_id: str) -> Dict[str, Any]:
        """Deleta (soft delete) um template."""
        payload = {"id": template_id}
        response = self.delete(f"/templates/{template_id}", json=payload)
        return response.json() if response.text else {}

    # ==================== EMAIL SENDING (Sync) ====================

    def send_email(
        self,
        to: List[str],
        subject: str,
        body: Optional[str] = None,
        html: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        template_id: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Envia um email de forma síncrona.

        Args:
            to: Lista de destinatários
            subject: Assunto (ignorado se usar template)
            body: Corpo em texto
            html: Corpo em HTML
            cc: Cópia
            bcc: Cópia oculta
            template_id: ID do template (opcional)
            variables: Variáveis para template
            attachments: Anexos

        Returns:
            Resposta com messageId/trackingId e status
        """
        payload = {"to": to}

        if template_id:
            payload["templateId"] = template_id
            if variables:
                payload["variables"] = variables
        else:
            payload["subject"] = subject
            if body:
                payload["body"] = body
            if html:
                payload["html"] = html

        if cc:
            payload["cc"] = cc
        if bcc:
            payload["bcc"] = bcc
        if attachments:
            payload["attachments"] = attachments

        response = self.post("/emails/send", json=payload)
        return response.json()

    # ==================== EMAIL QUEUE (Async) ====================

    def queue_email(
        self,
        to: List[Dict[str, str]],
        subject: Optional[str] = None,
        text_content: Optional[str] = None,
        template_id: Optional[str] = None,
        template_variables: Optional[Dict[str, Any]] = None,
        priority: str = "medium",
        track_opens: bool = False,
        track_clicks: bool = False
    ) -> Dict[str, Any]:
        """
        Adiciona um email único na fila.

        Args:
            to: Lista de destinatários [{"email": "...", "name": "..."}]
            subject: Assunto
            text_content: Conteúdo em texto
            template_id: ID do template
            template_variables: Variáveis do template
            priority: Prioridade (low, medium, high, urgent)
            track_opens: Rastrear aberturas
            track_clicks: Rastrear cliques

        Returns:
            Resposta com trackingId/queueId
        """
        payload = {
            "to": to,
            "priority": priority
        }

        if template_id:
            payload["templateId"] = template_id
            if template_variables:
                payload["templateVariables"] = template_variables
        else:
            if subject:
                payload["subject"] = subject
            if text_content:
                payload["textContent"] = text_content

        if track_opens:
            payload["trackOpens"] = track_opens
        if track_clicks:
            payload["trackClicks"] = track_clicks

        response = self.post("/emails", json=payload)
        return response.json()

    def get_email_status(self, tracking_id: str) -> Dict[str, Any]:
        """Consulta o status de um email na fila."""
        response = self.get(f"/emails/{tracking_id}")
        return response.json()

    def queue_bulk_emails(
        self,
        template_id: str,
        recipients: List[Dict[str, Any]],
        batch_size: int = 100,
        batch_delay: int = 5,
        priority: str = "medium",
        track_opens: bool = False,
        track_clicks: bool = False
    ) -> Dict[str, Any]:
        """
        Adiciona emails em massa na fila.

        Args:
            template_id: ID do template
            recipients: Lista de destinatários com variables
            batch_size: Tamanho do lote
            batch_delay: Delay entre lotes (segundos)
            priority: Prioridade
            track_opens: Rastrear aberturas
            track_clicks: Rastrear cliques

        Returns:
            Resposta com batchId/bulkTrackingId
        """
        payload = {
            "templateId": template_id,
            "recipients": recipients,
            "batchSize": batch_size,
            "batchDelay": batch_delay,
            "priority": priority,
            "trackOpens": track_opens,
            "trackClicks": track_clicks
        }

        response = self.post("/emails/bulk", json=payload)
        return response.json()

    def get_bulk_status(self, batch_id: str) -> Dict[str, Any]:
        """Consulta o status de um envio em massa."""
        response = self.get(f"/emails/bulk/{batch_id}")
        return response.json()

    def schedule_email(
        self,
        to: List[Dict[str, str]],
        scheduled_for: str,
        timezone: str = "America/Sao_Paulo",
        subject: Optional[str] = None,
        template_id: Optional[str] = None,
        template_variables: Optional[Dict[str, Any]] = None,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """
        Agenda um email para envio futuro.

        Args:
            to: Lista de destinatários
            scheduled_for: Data/hora agendada (ISO 8601)
            timezone: Timezone
            subject: Assunto
            template_id: ID do template
            template_variables: Variáveis do template
            priority: Prioridade

        Returns:
            Resposta com scheduleId
        """
        payload = {
            "to": to,
            "scheduledFor": scheduled_for,
            "timezone": timezone,
            "priority": priority
        }

        if template_id:
            payload["templateId"] = template_id
            if template_variables:
                payload["templateVariables"] = template_variables
        else:
            if subject:
                payload["subject"] = subject

        response = self.post("/emails/scheduled", json=payload)
        return response.json()

    def cancel_scheduled_email(self, schedule_id: str) -> Dict[str, Any]:
        """Cancela um email agendado."""
        response = self.delete(f"/emails/scheduled/{schedule_id}")
        return response.json() if response.text else {}
