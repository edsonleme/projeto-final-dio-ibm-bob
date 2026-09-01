"""
dio-explorer/mcp/auth.py
========================
Middleware de autenticação para o modo HTTP/SSE do servidor MCP.

Modos suportados:
  api_key  (padrão) — header  X-API-Key  comparado a DIO_API_KEY env var
  oidc               — preparado para OpenID Connect / SSO (extensão futura)

Configuração via variáveis de ambiente:
  DIO_AUTH_MODE   = "api_key" | "oidc" | "none"   (padrão: "api_key")
  DIO_API_KEY     = <chave secreta>                (obrigatório em api_key)

  # OIDC (futuro)
  DIO_OIDC_ISSUER    = https://seu-idp.exemplo.com
  DIO_OIDC_AUDIENCE  = dio-explorer-api

Segurança:
  - A chave nunca é logada.
  - Comparação feita com hmac.compare_digest para evitar timing attacks.
  - Em modo "none" (apenas dev local) todos os requests são aceitos.
  - NUNCA exponha o servidor em 0.0.0.0 sem um reverse-proxy TLS na frente.
"""

import hmac
import logging
import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger("dio-mcp.auth")

_AUTH_MODE = os.environ.get("DIO_AUTH_MODE", "api_key").lower()
_API_KEY   = os.environ.get("DIO_API_KEY", "")


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware Starlette que aplica autenticação ao servidor HTTP/SSE.

    Rotas liberadas sem autenticação:
      GET /health  — health-check para load-balancers e probes k8s

    Todas as outras rotas exigem o header  X-API-Key  (modo api_key)
    ou Bearer JWT válido (modo oidc — futuro).
    """

    async def dispatch(self, request: Request, call_next):
        # Health-check público — sem auth
        if request.url.path == "/health":
            return await call_next(request)

        if _AUTH_MODE == "none":
            logger.warning(
                "Auth desativada (DIO_AUTH_MODE=none). Use apenas em dev local."
            )
            return await call_next(request)

        if _AUTH_MODE == "api_key":
            return await self._check_api_key(request, call_next)

        if _AUTH_MODE == "oidc":
            return await self._check_oidc(request, call_next)

        # Modo desconhecido — nega por padrão (fail-secure)
        logger.error("DIO_AUTH_MODE='%s' não reconhecido. Negando acesso.", _AUTH_MODE)
        return JSONResponse({"error": "Configuração de autenticação inválida."}, status_code=500)

    # ------------------------------------------------------------------
    # API Key
    # ------------------------------------------------------------------

    async def _check_api_key(self, request: Request, call_next):
        if not _API_KEY:
            logger.error(
                "DIO_API_KEY não configurada. Defina a variável de ambiente antes de "
                "iniciar o servidor em modo HTTP."
            )
            return JSONResponse(
                {"error": "Servidor sem chave de API configurada."},
                status_code=500,
            )

        provided = request.headers.get("X-API-Key", "")

        # hmac.compare_digest previne timing attacks
        if not hmac.compare_digest(
            provided.encode("utf-8"),
            _API_KEY.encode("utf-8"),
        ):
            logger.warning(
                "Tentativa de acesso com X-API-Key inválida. IP: %s",
                request.client.host if request.client else "desconhecido",
            )
            return JSONResponse(
                {"error": "Não autorizado. Forneça X-API-Key válida."},
                status_code=401,
            )

        return await call_next(request)

    # ------------------------------------------------------------------
    # OIDC / SSO — extensão futura
    # ------------------------------------------------------------------

    async def _check_oidc(self, request: Request, call_next):
        """
        Placeholder para autenticação OpenID Connect (SSO).

        Implementação futura deve:
        1. Extrair o Bearer token do header Authorization.
        2. Validar assinatura e claims via PyJWT + chaves públicas do issuer
           (JWKS endpoint: {DIO_OIDC_ISSUER}/.well-known/jwks.json).
        3. Verificar 'aud' == DIO_OIDC_AUDIENCE e 'exp' não expirado.
        4. Injetar o subject/claims no request.state para uso nas tools.

        Dependências a adicionar em requirements.txt:
          python-jose[cryptography] ou PyJWT[crypto] >= 2.8
        """
        logger.warning(
            "Modo OIDC ainda não implementado. Configure DIO_AUTH_MODE=api_key."
        )
        return JSONResponse(
            {"error": "Modo OIDC não implementado nesta versão."},
            status_code=501,
        )
