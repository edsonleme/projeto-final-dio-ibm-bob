"""
Ferramentas MCP: trilha
Expõe buscar_trilhas() e listar_tecnologias() via MCPServer.tool() (API v2).
"""

import json
import logging
import os
import sys

from mcp.server.mcpserver import MCPServer

logger = logging.getLogger("dio-mcp.trilha")

_DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "trails_dio.json"
)


def register_trilha(server: MCPServer) -> None:

    @server.tool(description=(
        "Busca trilhas DIO pela tecnologia (ex.: 'Java', 'Python', 'AWS'). "
        "Retorna metadados completos: nome, nível, módulos, XP, badges, "
        "lives ao vivo e promoções ativas. "
        "Se a tecnologia não for encontrada, retorna a lista de tecnologias disponíveis."
    ))
    def buscar_trilha(tecnologia: str) -> str:
        """
        tecnologia: Nome ou parte do nome da tecnologia (busca case-insensitive).
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
        from dio_explorer import buscar_trilhas, listar_tecnologias

        tecnologia = (tecnologia or "").strip()
        if not tecnologia:
            return json.dumps({"error": "Parâmetro tecnologia é obrigatório."}, ensure_ascii=False)

        try:
            trilhas = buscar_trilhas(tecnologia, _DATA_FILE)
        except ValueError as exc:
            return json.dumps({"error": str(exc)}, ensure_ascii=False)

        if not trilhas:
            disponiveis = listar_tecnologias(_DATA_FILE)
            return json.dumps({
                "encontrado": False,
                "tecnologia_buscada": tecnologia,
                "tecnologias_disponiveis": disponiveis,
            }, ensure_ascii=False)

        return json.dumps(
            {"encontrado": True, "trilhas": trilhas},
            ensure_ascii=False,
            default=str,
        )

    @server.tool(description=(
        "Lista todas as tecnologias disponíveis no catálogo DIO. "
        "Use antes de buscar_trilha para descobrir o nome exato da tecnologia."
    ))
    def listar_tecnologias() -> str:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
        from dio_explorer import listar_tecnologias as _listar

        return json.dumps(_listar(_DATA_FILE), ensure_ascii=False)
