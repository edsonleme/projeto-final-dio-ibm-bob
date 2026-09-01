# DIO Explorer — Projeto Final DIO + IBM Bob

> Projeto final do bootcamp **DIO + IBM** desenvolvido com o assistente **IBM Bob**.
> Simula um sistema de aprendizado gamificado da plataforma [Digital Innovation One](https://www.dio.me).

![Python 3.14](https://img.shields.io/badge/Python-3.14-blue)
![82 testes](https://img.shields.io/badge/testes-82%20passed-brightgreen)
![Cobertura](https://img.shields.io/badge/cobertura-100%25-brightgreen)
![MCP Server](https://img.shields.io/badge/MCP-Server-purple)

---

## O que é o DIO Explorer

O **DIO Explorer** é uma aplicação Python que oferece três funcionalidades principais para exploração de trilhas de aprendizagem:

- **`/trilha`** — apresenta um plano de estudos detalhado de acordo com a tecnologia escolhida
- **`/desafio`** — gera um desafio de código conforme a tecnologia e o nível informado
- **`/certificado`** — cria um certificado fictício para uma trilha concluída

Cada funcionalidade está disponível de **três formas**:

| Forma | Como usar |
|---|---|
| **Bob Command** | `/trilha Java`, `/desafio Python Iniciante`, `/certificado "Seu Nome" Java` |
| **Bob Skill** | Invocável via texto natural no chat do Bob |
| **MCP Tool** | Servidor MCP consumível por qualquer cliente compatível |

---

## Como executar o projeto

### Pré-requisitos

```bash
# Python 3.11 ou superior
python --version

# Instalar dependências do MCP Server
pip install -r dio-explorer/mcp/requirements.txt
```

### Clonar e configurar

```bash
git clone https://github.com/edsonleme/projeto-final-dio-ibm-bob.git
cd projeto-final-dio-ibm-bob
```

### Iniciar o MCP Server (modo stdio — gerenciado pelo Bob)

O Bob inicializa o servidor automaticamente via `.bob/mcp.json`. Nenhuma ação manual necessária.

### Iniciar o MCP Server (modo HTTP/SSE — acesso externo)

```bash
# Defina a chave de API (obrigatório — nunca hardcode)
export DIO_API_KEY="sua-chave-secreta-de-pelo-menos-32-caracteres"

# Inicie o servidor (bind em 127.0.0.1 por segurança)
python dio-explorer/mcp/server.py --http --port 8000

# Verifique se está rodando
curl http://127.0.0.1:8000/health
```

---

## Como usar os comandos

### /trilha — Plano de Estudos

```
/trilha Java
/trilha Python
/trilha AWS
```

Exibe: nível, módulos, XP total, badges, lives ao vivo, promoções ativas e um plano de estudos detalhado gerado para a trilha.

### /desafio — Desafio de Código

```
/desafio Java Intermediário
/desafio Python Iniciante
/desafio Kubernetes Avançado
```

Gera: enunciado, requisitos funcionais, dicas, critérios de avaliação, tempo estimado e XP do desafio.

| Nível | XP | Tempo |
|---|---|---|
| Iniciante | 100–300 XP | 15–30 min |
| Intermediário | 300–600 XP | 30–60 min |
| Avançado | 600–1200 XP | 60–120 min |

### /certificado — Certificado de Conclusão

```
/certificado "João Silva" Java
/certificado "Maria Souza" Python
/certificado "Carlos Lima" "Apache Spark"
```

Gera um certificado Markdown com código único (`DIO-{id}-{ano}-{6chars}`), badges conquistadas e mensagem personalizada. Oferece a opção de salvar em `dio-explorer/docs/certificados-emitidos/`.

---

## Como executar os testes

```bash
# Na pasta dio-explorer
cd dio-explorer
python run_tests.py
```

Ou diretamente com pytest:

```bash
pytest src/tests/ --cov=src --cov-report=term-missing --cov-fail-under=70
```

### Resultado atual

```
82 testes | 0 falhas | Cobertura: 100%

test_trilha.py       — 21 testes  (/trilha)
test_desafio.py      — 29 testes  (/desafio)
test_certificado.py  — 32 testes  (/certificado)
```

---

## Melhorias realizadas

Em relação ao escopo base do desafio, o projeto foi expandido com:

- **MCP Server completo** com 6 ferramentas expostas e dois modos de transporte (stdio e HTTP/SSE)
- **Autenticação segura** via `X-API-Key` com `hmac.compare_digest` para prevenir timing attacks
- **Git Flow estruturado** com 4 branches (`main`, `develop`, `homologacao`, `production`) e proteções no GitHub
- **100% de cobertura** de testes (meta mínima era 70%)
- **Catálogo de 20 trilhas** cobrindo tecnologias populares: Python, Java, React, AWS, Docker, Kubernetes, Apache Spark, etc.
- **Documentação completa** em [`dio-explorer-ibm-bob-documentacao-completa-do-projeto.md`](dio-explorer-ibm-bob-documentacao-completa-do-projeto.md) com todos os 12 prompts usados, dicas de uso do Bob e insights para futuros profissionais

---

## O que aprendi durante o desafio

**1. IA como pair programmer, não substituto**
O Bob não substitui o raciocínio do desenvolvedor — ele acelera a execução. A arquitetura foi uma decisão humana; o Bob implementou com qualidade e velocidade. Saber o que pedir é o diferencial.

**2. Testes são inegociáveis, mesmo com IA**
Com código gerado por IA, os testes ganham importância ainda maior: são a garantia de que o código faz o que foi pedido.

**3. MCP é o protocolo de integração do futuro**
Construir um MCP Server transforma uma aplicação Python em uma "extensão nativa" de qualquer assistente compatível — não apenas o Bob.

**4. Segurança desde o início**
Binding em `127.0.0.1`, secrets via variáveis de ambiente, `hmac.compare_digest`, fail-secure por padrão. Pequenos descuidos em segurança têm grandes consequências.

**5. Documentação é parte do código**
Skills, Commands e READMEs são documentação executável. O Bob os lê e executa — a mesma disciplina de código limpo deve ser aplicada à documentação.

---

## Estrutura do projeto

```
projeto-final-dio-ibm-bob/
├── README.md                        ← este arquivo
├── .bob/
│   ├── mcp.json                     ← registro do MCP Server no Bob
│   ├── commands/                    ← slash commands (/trilha, /desafio, /certificado)
│   └── skills/                      ← skills invocáveis por texto natural
└── dio-explorer/
    ├── data/trails_dio.json         ← catálogo de 20 trilhas fictícias
    ├── src/
    │   ├── dio_explorer.py          ← lógica de negócio (Python puro, testável)
    │   └── tests/                   ← 82 testes unitários
    ├── mcp/
    │   ├── server.py                ← entrypoint MCP (stdio + HTTP/SSE)
    │   ├── auth.py                  ← middleware de autenticação
    │   └── tools/                   ← 6 MCP tools
    └── docs/
        ├── test_results.txt         ← relatório de testes
        └── certificados-emitidos/   ← certificados gerados
```

---

## 🌿 Git Flow

### Branches

| Branch | Ambiente | Propósito |
|---|---|---|
| `main` | — | Ponto de origem do projeto |
| `develop` | Desenvolvimento | Integração contínua de features |
| `homologacao` | QA | Validação antes de produção |
| `production` | Produção | Código estável e aprovado |

### Fluxo

```
feature/* ou fix/*
       │
       ▼
    develop  ──────►  homologacao  ──────►  production
  (dev / CI)          (QA / testes)         (estável)
```

Todo código entra via **Pull Request**. Nenhum push direto é permitido nas branches protegidas.

### Convenção de nomenclatura

| Prefixo | Uso |
|---|---|
| `feature/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `hotfix/` | Correção urgente em produção |
| `docs/` | Atualização de documentação |
| `chore/` | Manutenção (deps, configs) |

---

*Projeto Final — DIO + IBM Bootcamp · Desenvolvido com IBM Bob*
