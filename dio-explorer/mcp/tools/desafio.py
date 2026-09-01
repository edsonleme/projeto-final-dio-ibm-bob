"""
Ferramentas MCP: desafio
Expõe gerar_desafio() e validar_nivel() via MCPServer.tool() (API v2).
"""

import json
import logging
import os
import sys

from mcp.server.mcpserver import MCPServer

logger = logging.getLogger("dio-mcp.desafio")

_DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "trails_dio.json"
)


def register_desafio(server: MCPServer) -> None:

    @server.tool(description=(
        "Gera os metadados de um desafio de código para a tecnologia e nível informados. "
        "Níveis aceitos: Iniciante, Intermediário, Avançado. "
        "Retorna: tecnologia, nivel, xp, tempo_estimado, trilha_encontrada."
    ))
    def gerar_desafio(tecnologia: str, nivel: str) -> str:
        """
        tecnologia: Tecnologia do desafio (ex.: 'Java', 'Python').
        nivel: Nível de dificuldade — Iniciante, Intermediário ou Avançado.
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
        from dio_explorer import gerar_desafio as _gerar

        tecnologia = (tecnologia or "").strip()
        nivel = (nivel or "").strip()

        if not tecnologia or not nivel:
            return json.dumps(
                {"error": "Parâmetros tecnologia e nivel são obrigatórios."},
                ensure_ascii=False,
            )

        try:
            resultado = _gerar(tecnologia, nivel, _DATA_FILE)
            # Omite a lista completa de trilhas (muito verbosa via MCP)
            resultado_slim = {k: v for k, v in resultado.items() if k != "trilhas"}
            return json.dumps(resultado_slim, ensure_ascii=False)
        except ValueError as exc:
            return json.dumps({"error": str(exc)}, ensure_ascii=False)

    @server.tool(description=(
        "Verifica se um nível de dificuldade é válido para os desafios DIO. "
        "Aceita: Iniciante, Intermediário, Avançado (case-insensitive). "
        "Retorna {valido: true/false}."
    ))
    def validar_nivel(nivel: str) -> str:
        """
        nivel: Nível a validar (ex.: 'Iniciante', 'intermediário', 'AVANÇADO').
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
        from dio_explorer import validar_nivel as _validar

        return json.dumps({"valido": _validar(nivel or "")}, ensure_ascii=False)
