"""
Testes unitários para o comando /certificado
Cobre: gerar_certificado(), renderizar_certificado_md()
"""

import pytest
import sys
import os
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dio_explorer import gerar_certificado, renderizar_certificado_md

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "trails_dio.json"
)

NOME_ALUNO = "João Silva"
TECNOLOGIA = "Java"


# ---------------------------------------------------------------------------
# gerar_certificado — cenários de sucesso
# ---------------------------------------------------------------------------


class TestGerarCertificadoSucesso:

    def test_retorna_dict(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        assert isinstance(cert, dict)

    def test_nome_aluno_no_certificado(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        assert cert["nome_aluno"] == NOME_ALUNO

    def test_tecnologia_no_certificado(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        assert "Java" in cert["tecnologia"]

    def test_nome_trilha_preenchido(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        assert cert["nome_trilha"] != ""

    def test_nivel_preenchido(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        assert cert["nivel"] in ("Iniciante", "Intermediário", "Avançado")

    def test_modulos_positivo(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        assert cert["modulos"] > 0

    def test_xp_total_positivo(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        assert cert["xp_total"] > 0

    def test_badges_e_lista_nao_vazia(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        assert isinstance(cert["badges"], list)
        assert len(cert["badges"]) > 0

    def test_data_formato_dd_mm_aaaa(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        partes = cert["data"].split("/")
        assert len(partes) == 3
        dia, mes, ano = partes
        assert len(dia) == 2
        assert len(mes) == 2
        assert len(ano) == 4

    def test_data_e_hoje(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        hoje = datetime.date.today().strftime("%d/%m/%Y")
        assert cert["data"] == hoje

    def test_codigo_formato_dio_id_ano_sufixo(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        codigo = cert["codigo"]
        partes = codigo.split("-")
        assert partes[0] == "DIO", f"Prefixo inválido: {partes[0]}"
        assert partes[1].isdigit(), f"ID não é numérico: {partes[1]}"
        assert len(partes[2]) == 4, f"Ano com formato inválido: {partes[2]}"
        assert len(partes[3]) == 6, f"Sufixo deve ter 6 chars: {partes[3]}"

    def test_codigo_sufixo_maiusculo(self):
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        sufixo = cert["codigo"].split("-")[3]
        assert sufixo == sufixo.upper()

    def test_campos_obrigatorios_presentes(self):
        campos = {
            "nome_aluno", "nome_trilha", "tecnologia", "nivel",
            "modulos", "xp_total", "badges", "data", "codigo"
        }
        cert = gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)
        for campo in campos:
            assert campo in cert, f"Campo '{campo}' ausente no certificado."

    def test_busca_case_insensitive(self):
        cert_upper = gerar_certificado(NOME_ALUNO, "JAVA", DATA_PATH)
        cert_lower = gerar_certificado(NOME_ALUNO, "java", DATA_PATH)
        assert cert_upper["nome_trilha"] == cert_lower["nome_trilha"]

    def test_nome_aluno_com_espacos_extras_e_normalizado(self):
        cert = gerar_certificado("  João Silva  ", TECNOLOGIA, DATA_PATH)
        assert cert["nome_aluno"] == "João Silva"


# ---------------------------------------------------------------------------
# gerar_certificado — cenários de erro
# ---------------------------------------------------------------------------


class TestGerarCertificadoErros:

    def test_tecnologia_inexistente_levanta_value_error(self):
        with pytest.raises(ValueError, match="não encontrada"):
            gerar_certificado(NOME_ALUNO, "COBOL", DATA_PATH)

    def test_nome_vazio_levanta_value_error(self):
        with pytest.raises(ValueError, match="não pode ser vazio"):
            gerar_certificado("", TECNOLOGIA, DATA_PATH)

    def test_nome_apenas_espacos_levanta_value_error(self):
        with pytest.raises(ValueError, match="não pode ser vazio"):
            gerar_certificado("   ", TECNOLOGIA, DATA_PATH)

    def test_mensagem_erro_lista_tecnologias_disponiveis(self):
        with pytest.raises(ValueError) as exc_info:
            gerar_certificado(NOME_ALUNO, "XYZ_TECH_INEXISTENTE", DATA_PATH)
        assert "Disponíveis:" in str(exc_info.value)


# ---------------------------------------------------------------------------
# renderizar_certificado_md
# ---------------------------------------------------------------------------


class TestRenderizarCertificadoMd:

    @pytest.fixture
    def cert(self):
        return gerar_certificado(NOME_ALUNO, TECNOLOGIA, DATA_PATH)

    def test_retorna_string(self, cert):
        md = renderizar_certificado_md(cert)
        assert isinstance(md, str)

    def test_contem_nome_aluno(self, cert):
        md = renderizar_certificado_md(cert)
        assert NOME_ALUNO in md

    def test_contem_nome_trilha(self, cert):
        md = renderizar_certificado_md(cert)
        assert cert["nome_trilha"] in md

    def test_contem_tecnologia(self, cert):
        md = renderizar_certificado_md(cert)
        assert cert["tecnologia"] in md

    def test_contem_nivel(self, cert):
        md = renderizar_certificado_md(cert)
        assert cert["nivel"] in md

    def test_contem_codigo_certificado(self, cert):
        md = renderizar_certificado_md(cert)
        assert cert["codigo"] in md

    def test_contem_data(self, cert):
        md = renderizar_certificado_md(cert)
        assert cert["data"] in md

    def test_contem_todos_os_badges(self, cert):
        md = renderizar_certificado_md(cert)
        for badge in cert["badges"]:
            assert badge in md, f"Badge '{badge}' não encontrado no MD gerado."

    def test_contem_titulo_certificado(self, cert):
        md = renderizar_certificado_md(cert)
        assert "Certificado de Conclusão" in md

    def test_contem_assinatura_ficticia(self, cert):
        md = renderizar_certificado_md(cert)
        assert "DIO Explorer" in md

    def test_contem_url_verificacao(self, cert):
        md = renderizar_certificado_md(cert)
        assert "dio.me/certificate" in md


# ---------------------------------------------------------------------------
# Teste de integração ponta a ponta: /trilha -> /desafio -> /certificado
# ---------------------------------------------------------------------------


class TestFluxoCompleto:
    """
    Simula o fluxo completo do aluno:
    1. Consulta a trilha de Java
    2. Gera um desafio para Java Intermediário
    3. Gera o certificado para o aluno
    """

    def test_fluxo_trilha_desafio_certificado(self):
        from dio_explorer import buscar_trilhas, gerar_desafio

        # Passo 1 — /trilha Java
        trilhas = buscar_trilhas("Java", DATA_PATH)
        assert len(trilhas) > 0, "Trilha Java deve existir."
        trilha = trilhas[0]

        # Passo 2 — /desafio Java Intermediário
        desafio = gerar_desafio("Java", trilha["nivel"], DATA_PATH)
        assert desafio["trilha_encontrada"] is True
        assert 300 <= desafio["xp"] <= 600

        # Passo 3 — /certificado João Silva Java
        cert = gerar_certificado("João Silva", "Java", DATA_PATH)
        md = renderizar_certificado_md(cert)

        assert "João Silva" in md
        assert trilha["nome"] in md
        assert cert["codigo"].startswith("DIO-")
        assert len(md) > 200, "Certificado MD deve ter conteúdo substancial."
