#!/usr/bin/env python3
"""
DIO Explorer MCP Server
=======================
Expõe as funcionalidades do DIO Explorer como ferramentas MCP,
permitindo integração com Bob (stdio), e preparado para
transporte HTTP/SSE (HTTPS + API Key / SSO futuramente).

Transporte padrão : stdio (Bob spawna o processo)
Transporte HTTP   : ative com --http [--port PORT] (requer uvicorn)

Autenticação HTTP : via header  X-API-Key  (lido de DIO_API_KEY env var)
                    SSO/OAuth   : extensão futura via DIO_AUTH_MODE=oidc
"""

import argparse
import logging
import os
import sys

# Garante que o módulo de negócio seja encontrado independente do cwd
_ROOT = os.path.dirname(os.path.abspath(__file__))
_SRC  = os.path.join(_ROOT, "..", "src")
sys.path.insert(0, _SRC)
sys.path.insert(0, _ROOT)  # para importar auth.py

from mcp.server.mcpserver import MCPServer

import tools  # ferramentas registradas em tools/__init__.py

# ---------------------------------------------------------------------------
# Logging — sempre para stderr para não poluir o canal stdio do protocolo MCP
# ---------------------------------------------------------------------------
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[DIO-MCP] %(levelname)s %(message)s",
)
logger = logging.getLogger("dio-mcp")

# ---------------------------------------------------------------------------
# Instância do servidor MCP
# ---------------------------------------------------------------------------
app = MCPServer("dio-explorer", version="1.0.0")

# Registra todas as ferramentas definidas em tools/
tools.register_all(app)

# ---------------------------------------------------------------------------
# Entrypoint — stdio (padrão) ou HTTP
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DIO Explorer MCP Server")
    parser.add_argument(
        "--http",
        action="store_true",
        help="Inicia em modo HTTP/SSE em vez de stdio",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("DIO_MCP_PORT", "8000")),
        help="Porta HTTP (padrão: 8000 ou DIO_MCP_PORT env var)",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("DIO_MCP_HOST", "127.0.0.1"),
        help="Host de bind HTTP (padrão: 127.0.0.1 — nunca 0.0.0.0)",
    )
    return parser.parse_args()


def _run_http(host: str, port: int) -> None:
    """
    Inicia o servidor HTTP/SSE.
    Requer uvicorn (já incluído no requirements.txt).

    Segurança:
      - Bind apenas em localhost (127.0.0.1) por padrão.
      - Para expor externamente use um reverse-proxy (nginx/Caddy) com TLS.
      - Autenticação via X-API-Key header (middleware em auth.py).
    """
    try:
        import uvicorn
        from auth import ApiKeyMiddleware

        starlette_app = app.sse_app()
        starlette_app = ApiKeyMiddleware(starlette_app)

        logger.info("Iniciando HTTP/SSE em http://%s:%d/sse", host, port)
        logger.info("Protegido por X-API-Key (configure DIO_API_KEY)")
        uvicorn.run(starlette_app, host=host, port=port, log_level="warning")

    except ImportError as exc:
        logger.error("Dependência ausente para modo HTTP: %s", exc)
        logger.error("Execute:  pip install -r dio-explorer/mcp/requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    import asyncio

    args = _parse_args()
    if args.http:
        _run_http(args.host, args.port)
    else:
        logger.info("Iniciando em modo stdio")
        asyncio.run(app.run_stdio_async())
