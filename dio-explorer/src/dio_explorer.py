"""
DIO Explorer — módulo principal com as funções de negócio
testáveis de forma independente dos comandos Bob.
"""

import json
import os
import re
import string
import random
import datetime

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "trails_dio.json"
)

NIVEIS_VALIDOS = {"iniciante", "intermediário", "avancado", "avançado"}

XP_RANGES = {
    "iniciante": (100, 300),
    "intermediário": (300, 600),
    "avancado": (600, 1200),
    "avançado": (600, 1200),
}

# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------


def _load_trails(filepath: str = DATA_FILE) -> dict:
    """Carrega o JSON de trilhas do disco e retorna o dict completo."""
    with open(filepath, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# /trilha — busca de trilhas por tecnologia
# ---------------------------------------------------------------------------


def buscar_trilhas(tecnologia: str, filepath: str = DATA_FILE) -> list:
    """
    Retorna lista de trilhas cujo campo `tecnologia` contenha o termo
    informado (busca case-insensitive).

    Parâmetros
    ----------
    tecnologia : str
        Termo de busca (ex.: "Java").
    filepath : str
        Caminho para o arquivo JSON de trilhas.

    Retorna
    -------
    list[dict]  — pode ser vazia se nenhuma trilha for encontrada.
    """
    if not tecnologia or not tecnologia.strip():
        raise ValueError("O parâmetro 'tecnologia' não pode ser vazio.")

    data = _load_trails(filepath)
    termo = tecnologia.strip().lower()
    return [t for t in data["trails"] if termo in t["tecnologia"].lower()]


def listar_tecnologias(filepath: str = DATA_FILE) -> list:
    """Retorna lista de todas as tecnologias disponíveis no JSON."""
    data = _load_trails(filepath)
    return sorted({t["tecnologia"] for t in data["trails"]})


# ---------------------------------------------------------------------------
# /desafio — geração de desafio por tecnologia e nível
# ---------------------------------------------------------------------------


def validar_nivel(nivel: str) -> bool:
    """
    Valida se o nível informado é aceito.
    Aceita: Iniciante, Intermediário, Avançado (case-insensitive).
    """
    return nivel.strip().lower() in NIVEIS_VALIDOS


def calcular_xp_desafio(nivel: str, seed: int | None = None) -> int:
    """
    Calcula o XP do desafio dentro da faixa correspondente ao nível.
    `seed` é opcional e serve apenas para tornar os testes determinísticos.
    """
    if not validar_nivel(nivel):
        raise ValueError(f"Nível inválido: '{nivel}'. Use: Iniciante, Intermediário ou Avançado.")

    rng = random.Random(seed)
    nivel_key = nivel.strip().lower()
    low, high = XP_RANGES[nivel_key]
    return rng.randint(low, high)


def gerar_desafio(tecnologia: str, nivel: str, filepath: str = DATA_FILE) -> dict:
    """
    Valida os parâmetros e retorna um dict com os metadados do desafio
    (enunciado gerado programaticamente para fins de teste).

    Retorna
    -------
    dict com chaves: tecnologia, nivel, xp, tempo_estimado, trilha_encontrada
    """
    if not validar_nivel(nivel):
        raise ValueError(f"Nível inválido: '{nivel}'. Aceitos: Iniciante, Intermediário, Avançado.")

    trilhas = buscar_trilhas(tecnologia, filepath)

    nivel_key = nivel.strip().lower()
    tempos = {
        "iniciante": "15–30 min",
        "intermediário": "30–60 min",
        "avancado": "60–120 min",
        "avançado": "60–120 min",
    }

    return {
        "tecnologia": tecnologia,
        "nivel": nivel,
        "xp": calcular_xp_desafio(nivel),
        "tempo_estimado": tempos[nivel_key],
        "trilha_encontrada": len(trilhas) > 0,
        "trilhas": trilhas,
    }


# ---------------------------------------------------------------------------
# /certificado — geração de certificado fictício
# ---------------------------------------------------------------------------


def _gerar_codigo_certificado(trail_id: int) -> str:
    """Gera o código alfanumérico do certificado (ex.: DIO-2-2025-AB12CD)."""
    ano = datetime.date.today().year
    chars = string.ascii_uppercase + string.digits
    sufixo = "".join(random.choices(chars, k=6))
    return f"DIO-{trail_id}-{ano}-{sufixo}"


def gerar_certificado(nome_aluno: str, tecnologia: str, filepath: str = DATA_FILE) -> dict:
    """
    Busca a trilha e monta o dict de dados para o certificado.

    Retorna
    -------
    dict com todos os campos necessários para montar o certificado Markdown.

    Levanta
    -------
    ValueError  se nenhuma trilha for encontrada para a tecnologia.
    """
    if not nome_aluno or not nome_aluno.strip():
        raise ValueError("O nome do aluno não pode ser vazio.")

    trilhas = buscar_trilhas(tecnologia, filepath)
    if not trilhas:
        disponiveis = listar_tecnologias(filepath)
        raise ValueError(
            f"Tecnologia '{tecnologia}' não encontrada. "
            f"Disponíveis: {', '.join(disponiveis)}"
        )

    trilha = trilhas[0]
    hoje = datetime.date.today().strftime("%d/%m/%Y")

    return {
        "nome_aluno": nome_aluno.strip(),
        "nome_trilha": trilha["nome"],
        "tecnologia": trilha["tecnologia"],
        "nivel": trilha["nivel"],
        "modulos": trilha["modulos"],
        "xp_total": trilha["xp_total"],
        "badges": trilha["badges"],
        "data": hoje,
        "codigo": _gerar_codigo_certificado(trilha["id"]),
    }


def renderizar_certificado_md(cert: dict) -> str:
    """Converte o dict do certificado para texto Markdown."""
    badges_md = "\n".join(f"🏅 {b}" for b in cert["badges"])
    return (
        "# 📜 Certificado de Conclusão\n\n"
        f"> *A Digital Innovation One certifica que*\n\n"
        f"## {cert['nome_aluno']}\n\n"
        f"> *concluiu com êxito a trilha de aprendizado*\n\n"
        f"# {cert['nome_trilha']}\n\n"
        "---\n\n"
        f"| 🏷️ Tecnologia | {cert['tecnologia']} |\n"
        f"|---|---|\n"
        f"| 📊 Nível | {cert['nivel']} |\n"
        f"| 📦 Módulos | {cert['modulos']} módulos concluídos |\n"
        f"| ⭐ XP Obtido | {cert['xp_total']} XP |\n"
        f"| 📅 Data | {cert['data']} |\n"
        f"| 🔑 Código | {cert['codigo']} |\n\n"
        "---\n\n"
        "### 🏅 Badges Conquistadas\n\n"
        f"{badges_md}\n\n"
        "---\n\n"
        "*Certificado fictício gerado pelo DIO Explorer — IBM Bob Project*\n"
        "*Verifique autenticidade em: https://www.dio.me/certificate*\n"
    )
