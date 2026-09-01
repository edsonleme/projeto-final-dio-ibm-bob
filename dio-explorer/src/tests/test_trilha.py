"""
Testes unitários para o comando /trilha
Cobre: buscar_trilhas() e listar_tecnologias()
"""

import pytest
import sys
import os

# garante que o módulo pai seja encontrado
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dio_explorer import buscar_trilhas, listar_tecnologias

# ---------------------------------------------------------------------------
# Fixture — caminho do JSON real
# ---------------------------------------------------------------------------

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "trails_dio.json"
)


# ---------------------------------------------------------------------------
# buscar_trilhas — cenários de sucesso
# ---------------------------------------------------------------------------


class TestBuscarTrilhasEncontradas:
    """O termo de busca casa com trilhas existentes no JSON."""

    def test_busca_java_retorna_lista_nao_vazia(self):
        resultado = buscar_trilhas("Java", DATA_PATH)
        assert len(resultado) > 0, "Deve retornar ao menos uma trilha para 'Java'."

    def test_busca_java_retorna_apenas_trilhas_java(self):
        resultado = buscar_trilhas("Java", DATA_PATH)
        for trilha in resultado:
            assert "java" in trilha["tecnologia"].lower(), (
                f"Trilha retornada não contém 'Java': {trilha['tecnologia']}"
            )

    def test_busca_case_insensitive_java(self):
        resultado_upper = buscar_trilhas("JAVA", DATA_PATH)
        resultado_lower = buscar_trilhas("java", DATA_PATH)
        assert len(resultado_upper) == len(resultado_lower), (
            "Busca deve ser case-insensitive."
        )

    def test_busca_java_campos_obrigatorios_presentes(self):
        campos = {"id", "nome", "home", "tecnologia", "nivel", "modulos", "xp_total", "badges"}
        resultado = buscar_trilhas("Java", DATA_PATH)
        for trilha in resultado:
            for campo in campos:
                assert campo in trilha, f"Campo '{campo}' ausente na trilha retornada."

    def test_busca_java_nivel_intermediario(self):
        """A trilha Java do dataset é de nível Intermediário."""
        resultado = buscar_trilhas("Java", DATA_PATH)
        assert resultado[0]["nivel"] == "Intermediário"

    def test_busca_java_xp_total_positivo(self):
        resultado = buscar_trilhas("Java", DATA_PATH)
        assert resultado[0]["xp_total"] > 0

    def test_busca_java_modulos_positivo(self):
        resultado = buscar_trilhas("Java", DATA_PATH)
        assert resultado[0]["modulos"] > 0

    def test_busca_java_badges_e_lista(self):
        resultado = buscar_trilhas("Java", DATA_PATH)
        assert isinstance(resultado[0]["badges"], list)
        assert len(resultado[0]["badges"]) > 0

    def test_busca_java_home_e_url_valida(self):
        resultado = buscar_trilhas("Java", DATA_PATH)
        assert resultado[0]["home"].startswith("https://")

    def test_busca_python_retorna_resultado(self):
        resultado = buscar_trilhas("Python", DATA_PATH)
        assert len(resultado) > 0

    def test_busca_aws_retorna_resultado(self):
        resultado = buscar_trilhas("AWS", DATA_PATH)
        assert len(resultado) > 0

    def test_busca_parcial_retorna_resultado(self):
        """'Spark' deve encontrar a trilha 'Apache Spark'."""
        resultado = buscar_trilhas("Spark", DATA_PATH)
        assert len(resultado) > 0


# ---------------------------------------------------------------------------
# buscar_trilhas — cenários de trilha não encontrada
# ---------------------------------------------------------------------------


class TestBuscarTrilhasNaoEncontradas:

    def test_tecnologia_inexistente_retorna_lista_vazia(self):
        resultado = buscar_trilhas("COBOL", DATA_PATH)
        assert resultado == []

    def test_tecnologia_com_espacos_extras_retorna_lista_vazia(self):
        resultado = buscar_trilhas("   xyz_nao_existe   ", DATA_PATH)
        assert resultado == []

    def test_tecnologia_numerica_retorna_lista_vazia(self):
        resultado = buscar_trilhas("12345", DATA_PATH)
        assert resultado == []


# ---------------------------------------------------------------------------
# buscar_trilhas — entradas inválidas
# ---------------------------------------------------------------------------


class TestBuscarTrilhasEntradaInvalida:

    def test_tecnologia_vazia_levanta_value_error(self):
        with pytest.raises(ValueError):
            buscar_trilhas("", DATA_PATH)

    def test_tecnologia_somente_espacos_levanta_value_error(self):
        with pytest.raises(ValueError):
            buscar_trilhas("   ", DATA_PATH)


# ---------------------------------------------------------------------------
# listar_tecnologias
# ---------------------------------------------------------------------------


class TestListarTecnologias:

    def test_retorna_lista_nao_vazia(self):
        resultado = listar_tecnologias(DATA_PATH)
        assert len(resultado) > 0

    def test_retorna_lista_de_strings(self):
        resultado = listar_tecnologias(DATA_PATH)
        for item in resultado:
            assert isinstance(item, str)

    def test_sem_duplicatas(self):
        resultado = listar_tecnologias(DATA_PATH)
        assert len(resultado) == len(set(resultado))

    def test_java_esta_na_lista(self):
        resultado = listar_tecnologias(DATA_PATH)
        assert "Java" in resultado

    def test_lista_esta_ordenada(self):
        resultado = listar_tecnologias(DATA_PATH)
        assert resultado == sorted(resultado)
