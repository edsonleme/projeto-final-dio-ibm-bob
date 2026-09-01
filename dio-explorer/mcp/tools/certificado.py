"""
Ferramentas MCP: certificado
Expõe gerar_certificado() e salvar_certificado() via MCPServer.tool() (API v2).
"""

import json
import logging
import os
import sys

from mcp.server.mcpserver import MCPServer

logger = logging.getLogger("dio-mcp.certificado")

_DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "trails_dio.json"
)

_CERTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "docs", "certificados-emitidos"
)


def register_certificado(server: MCPServer) -> None:

    @server.tool(description=(
        "Gera um certificado fictício de conclusão de trilha DIO para o aluno "
        "e tecnologia informados. Retorna os campos do certificado em JSON, "
        "incluindo código único, data, badges e XP obtido."
    ))
    def gerar_certificado(nome_aluno: str, tecnologia: str) -> str:
        """
        nome_aluno: Nome completo do aluno (ex.: 'João Silva').
        tecnologia: Tecnologia da trilha concluída (ex.: 'Java').
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
        from dio_explorer import gerar_certificado as _gerar

        nome_aluno = (nome_aluno or "").strip()
        tecnologia = (tecnologia or "").strip()

        if not nome_aluno or not tecnologia:
            return json.dumps(
                {"error": "Parâmetros nome_aluno e tecnologia são obrigatórios."},
                ensure_ascii=False,
            )

        try:
            cert = _gerar(nome_aluno, tecnologia, _DATA_FILE)
            return json.dumps(cert, ensure_ascii=False)
        except ValueError as exc:
            return json.dumps({"error": str(exc)}, ensure_ascii=False)

    @server.tool(description=(
        "Gera e salva o certificado de conclusão em Markdown no diretório "
        "dio-explorer/docs/certificados-emitidos/. "
        "Retorna o caminho do arquivo criado e o código do certificado."
    ))
    def salvar_certificado(nome_aluno: str, tecnologia: str) -> str:
        """
        nome_aluno: Nome completo do aluno (ex.: 'João Silva').
        tecnologia: Tecnologia da trilha concluída (ex.: 'Java').
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
        from dio_explorer import gerar_certificado as _gerar, renderizar_certificado_md

        nome_aluno = (nome_aluno or "").strip()
        tecnologia = (tecnologia or "").strip()

        if not nome_aluno or not tecnologia:
            return json.dumps(
                {"error": "Parâmetros nome_aluno e tecnologia são obrigatórios."},
                ensure_ascii=False,
            )

        try:
            cert = _gerar(nome_aluno, tecnologia, _DATA_FILE)
            md_content = renderizar_certificado_md(cert)
            nome_arquivo = nome_aluno.replace(" ", "-")
            caminho = os.path.join(_CERTS_DIR, f"certificado-{nome_arquivo}.md")
            os.makedirs(_CERTS_DIR, exist_ok=True)
            with open(caminho, "w", encoding="utf-8") as fh:
                fh.write(md_content)
            return json.dumps({
                "salvo": True,
                "caminho": caminho,
                "codigo": cert["codigo"],
            }, ensure_ascii=False)
        except ValueError as exc:
            return json.dumps({"error": str(exc)}, ensure_ascii=False)
