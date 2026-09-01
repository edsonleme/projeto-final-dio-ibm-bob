"""
dio-explorer/mcp/tools/__init__.py
Ponto de entrada que registra todas as ferramentas no servidor MCP.
"""

from mcp.server import Server

from .trilha import register_trilha
from .desafio import register_desafio
from .certificado import register_certificado


def register_all(server: Server) -> None:
    """Registra todas as ferramentas DIO no servidor MCP."""
    register_trilha(server)
    register_desafio(server)
    register_certificado(server)
