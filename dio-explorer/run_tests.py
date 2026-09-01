"""
Runner de testes do DIO Explorer.
Executa pytest com cobertura de código e grava o resultado em:
  dio-explorer/docs/test_results.txt
"""

import subprocess
import sys
import os
import datetime

# ---------------------------------------------------------------------------
# Configuração de caminhos
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))   # dio-explorer/
TESTS_DIR = os.path.join(ROOT, "src", "tests")
SRC_DIR   = os.path.join(ROOT, "src")
REPORT_FILE = os.path.join(ROOT, "docs", "test_results.txt")

os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)

# ---------------------------------------------------------------------------
# Execução dos testes
# ---------------------------------------------------------------------------

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cmd = [
    sys.executable, "-m", "pytest",
    TESTS_DIR,
    "--tb=short",        # traceback compacto
    "-v",                # verbose — exibe cada test
    f"--cov={SRC_DIR}",  # cobertura do módulo src
    "--cov-report=term-missing",  # imprime linhas não cobertas
    "--cov-fail-under=70",        # falha se cobertura < 70 %
    "--no-header",
]

print(f"\n{'='*70}")
print(f"  DIO Explorer — Suite de Testes Unitários")
print(f"  Iniciado em: {timestamp}")
print(f"{'='*70}\n")

result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)

stdout = result.stdout
stderr = result.stderr
exit_code = result.returncode

# Exibe no console
print(stdout)
if stderr:
    print("[STDERR]")
    print(stderr)

# ---------------------------------------------------------------------------
# Grava relatório em TXT
# ---------------------------------------------------------------------------

separador = "=" * 70

relatorio = f"""{separador}
  DIO EXPLORER — RELATÓRIO DE TESTES UNITÁRIOS
  Gerado em: {timestamp}
{separador}

COMANDOS TESTADOS
  /trilha  — busca de trilhas por tecnologia (ex.: Java)
  /desafio — geração de desafio por tecnologia e nível
  /certificado — geração de certificado fictício de conclusão

META DE COBERTURA: >= 70 %

{separador}
SAÍDA DO PYTEST
{separador}

{stdout}
"""

if stderr:
    relatorio += f"\n{separador}\nSTDERR\n{separador}\n{stderr}\n"

relatorio += f"""
{separador}
RESULTADO FINAL
{separador}
Código de saída: {exit_code}
Status: {"✅  PASSOU — cobertura >= 70 %" if exit_code == 0 else "❌  FALHOU — verifique os detalhes acima"}
{separador}
"""

with open(REPORT_FILE, "w", encoding="utf-8") as fh:
    fh.write(relatorio)

print(f"\nRelatório gravado em: {REPORT_FILE}")
sys.exit(exit_code)
