"""
Testes unitários para o comando /desafio
Cobre: validar_nivel(), calcular_xp_desafio(), gerar_desafio()
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dio_explorer import validar_nivel, calcular_xp_desafio, gerar_desafio

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "trails_dio.json"
)


# ---------------------------------------------------------------------------
# validar_nivel
# ---------------------------------------------------------------------------


class TestValidarNivel:

    def test_iniciante_valido(self):
        assert validar_nivel("Iniciante") is True

    def test_intermediario_valido(self):
        assert validar_nivel("Intermediário") is True

    def test_avancado_valido(self):
        assert validar_nivel("Avançado") is True

    def test_avancado_sem_acento_valido(self):
        assert validar_nivel("avancado") is True

    def test_case_insensitive_iniciante(self):
        assert validar_nivel("INICIANTE") is True

    def test_case_insensitive_intermediario(self):
        assert validar_nivel("intermediário") is True

    def test_nivel_invalido_retorna_false(self):
        assert validar_nivel("Expert") is False

    def test_nivel_vazio_retorna_false(self):
        assert validar_nivel("") is False

    def test_nivel_numero_retorna_false(self):
        assert validar_nivel("1") is False

    def test_nivel_com_espaco_invalido(self):
        assert validar_nivel("Nível 2") is False


# ---------------------------------------------------------------------------
# calcular_xp_desafio
# ---------------------------------------------------------------------------


class TestCalcularXpDesafio:

    def test_xp_iniciante_dentro_da_faixa(self):
        for _ in range(20):
            xp = calcular_xp_desafio("Iniciante")
            assert 100 <= xp <= 300, f"XP fora da faixa Iniciante: {xp}"

    def test_xp_intermediario_dentro_da_faixa(self):
        for _ in range(20):
            xp = calcular_xp_desafio("Intermediário")
            assert 300 <= xp <= 600, f"XP fora da faixa Intermediário: {xp}"

    def test_xp_avancado_dentro_da_faixa(self):
        for _ in range(20):
            xp = calcular_xp_desafio("Avançado")
            assert 600 <= xp <= 1200, f"XP fora da faixa Avançado: {xp}"

    def test_xp_e_inteiro(self):
        xp = calcular_xp_desafio("Iniciante")
        assert isinstance(xp, int)

    def test_nivel_invalido_levanta_value_error(self):
        with pytest.raises(ValueError):
            calcular_xp_desafio("Especialista")

    def test_seed_deterministica_retorna_mesmo_valor(self):
        xp1 = calcular_xp_desafio("Intermediário", seed=42)
        xp2 = calcular_xp_desafio("Intermediário", seed=42)
        assert xp1 == xp2


# ---------------------------------------------------------------------------
# gerar_desafio
# ---------------------------------------------------------------------------


class TestGerarDesafio:

    def test_desafio_java_intermediario_retorna_dict(self):
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        assert isinstance(resultado, dict)

    def test_desafio_java_trilha_encontrada(self):
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        assert resultado["trilha_encontrada"] is True

    def test_desafio_java_tecnologia_no_resultado(self):
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        assert resultado["tecnologia"] == "Java"

    def test_desafio_java_nivel_no_resultado(self):
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        assert resultado["nivel"] == "Intermediário"

    def test_desafio_java_xp_positivo(self):
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        assert resultado["xp"] > 0

    def test_desafio_java_xp_dentro_da_faixa_intermediario(self):
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        assert 300 <= resultado["xp"] <= 600

    def test_desafio_java_tempo_estimado_presente(self):
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        assert "tempo_estimado" in resultado
        assert resultado["tempo_estimado"] != ""

    def test_desafio_java_tempo_estimado_intermediario(self):
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        assert resultado["tempo_estimado"] == "30–60 min"

    def test_desafio_tecnologia_inexistente_trilha_nao_encontrada(self):
        resultado = gerar_desafio("COBOL", "Iniciante", DATA_PATH)
        assert resultado["trilha_encontrada"] is False

    def test_desafio_nivel_invalido_levanta_value_error(self):
        with pytest.raises(ValueError):
            gerar_desafio("Java", "Mestre", DATA_PATH)

    def test_desafio_iniciante_tempo_correto(self):
        resultado = gerar_desafio("Python", "Iniciante", DATA_PATH)
        assert resultado["tempo_estimado"] == "15–30 min"

    def test_desafio_avancado_tempo_correto(self):
        resultado = gerar_desafio("AWS", "Avançado", DATA_PATH)
        assert resultado["tempo_estimado"] == "60–120 min"

    def test_desafio_campos_obrigatorios_presentes(self):
        campos = {"tecnologia", "nivel", "xp", "tempo_estimado", "trilha_encontrada", "trilhas"}
        resultado = gerar_desafio("Java", "Intermediário", DATA_PATH)
        for campo in campos:
            assert campo in resultado, f"Campo '{campo}' ausente no resultado."
