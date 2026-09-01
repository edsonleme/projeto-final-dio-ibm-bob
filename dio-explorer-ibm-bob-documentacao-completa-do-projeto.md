# DIO Explorer × IBM Bob

**Documentação completa do Projeto Final — Bootcamp DIO + IBM**

![Python 3.14](https://img.shields.io/badge/Python-3.14-blue)
![MCP Server](https://img.shields.io/badge/MCP-Server-purple)
![82 testes · 100% cobertura](https://img.shields.io/badge/testes-82%20%C2%B7%20100%25%20cobertura-green)
![IBM Bob · Agent Mode](https://img.shields.io/badge/IBM%20Bob-Agent%20Mode-gray)
![Git Flow](https://img.shields.io/badge/Git-Flow-gray)

---

## Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Arquitetura e Estrutura de Arquivos](#2-arquitetura-e-estrutura-de-arquivos)
3. [Funcionalidades Implementadas](#3-funcionalidades-implementadas)
4. [Prompts Usados com o Bob — Catálogo Completo](#4-prompts-usados-com-o-bob--catálogo-completo)
5. [Skills Criadas](#5-skills-criadas-bobskills)
6. [Commands Criados](#6-commands-criados-bobcommands)
7. [MCP Server](#7-mcp-server)
8. [Testes e Cobertura](#8-testes-e-cobertura)
9. [Git Flow Adotado](#9-git-flow-adotado)
10. [Segurança](#10-segurança)
11. [Dicas de Uso do Bob](#11-dicas-de-uso-do-bob)
12. [Insights para Futuros Profissionais](#12-insights-para-futuros-profissionais)

---

| Testes unitários | Cobertura de código | Ferramentas MCP | Skills / Commands |
|:---:|:---:|:---:|:---:|
| **82** | **100%** | **6** | **3** |

---

## 1. Visão Geral do Projeto

O **DIO Explorer** é uma aplicação Python construída inteiramente com o assistente **IBM Bob** durante o Bootcamp DIO + IBM. Ela simula um sistema de aprendizado gamificado da plataforma [Digital Innovation One](https://www.dio.me), oferecendo três funcionalidades principais:

- **`/trilha`** — consulta planos de estudo de trilhas DIO por tecnologia
- **`/desafio`** — gera desafios de código com enunciado, requisitos, dicas e XP
- **`/certificado`** — emite certificados fictícios de conclusão em Markdown

> **O diferencial do projeto:** cada funcionalidade está disponível de *três formas* diferentes: como **Bob Command** (slash command), como **Bob Skill** (invocável por texto), e como **MCP Tool** (servidor MCP consumível por qualquer cliente compatível).

---

## 2. Arquitetura e Estrutura de Arquivos

```
projeto-final-dio-ibm-bob/
├── README.md                        ← Git Flow e instruções gerais
├── .bob/
│   ├── mcp.json                     ← Registro do servidor MCP no Bob
│   ├── commands/
│   │   ├── trilha.md                ← Slash command /trilha
│   │   ├── desafio.md               ← Slash command /desafio
│   │   └── certificado.md           ← Slash command /certificado
│   └── skills/
│       ├── trilha/SKILL.md          ← Skill "trilha"
│       ├── desafio/SKILL.md         ← Skill "desafio"
│       └── certificado/SKILL.md     ← Skill "certificado"
└── dio-explorer/
    ├── data/
    │   └── trails_dio.json          ← Catálogo de trilhas (20 trilhas)
    ├── src/
    │   ├── dio_explorer.py          ← Lógica de negócio (pura Python)
    │   └── tests/
    │       ├── test_trilha.py       ← 21 testes unitários
    │       ├── test_desafio.py      ← 29 testes unitários
    │       └── test_certificado.py  ← 32 testes unitários
    ├── mcp/
    │   ├── server.py                ← Entrypoint MCP (stdio + HTTP/SSE)
    │   ├── auth.py                  ← Middleware de autenticação
    │   ├── requirements.txt         ← Dependências Python
    │   └── tools/
    │       ├── trilha.py            ← MCP tools: buscar_trilha, listar_tecnologias
    │       ├── desafio.py           ← MCP tools: gerar_desafio, validar_nivel
    │       └── certificado.py       ← MCP tools: gerar_certificado, salvar_certificado
    └── docs/
        ├── test_results.txt         ← Relatório de testes executados
        ├── desafio-Joao-Silva-Java-Intermediario.md
        └── certificados-emitidos/
            └── certificado-Joao-Silva.md
```

### Camadas da arquitetura

```
Bob UI (chat) → Command / Skill → MCP Tool (server.py) → dio_explorer.py (lógica) → trails_dio.json (dados)
```

A lógica de negócio em `dio_explorer.py` é **totalmente independente** do Bob e do MCP — pode ser testada com pytest puro e reutilizada em qualquer contexto Python.

---

## 3. Funcionalidades Implementadas

### /trilha — Plano de Estudos

| Função Python | O que faz |
|---|---|
| `buscar_trilhas(tecnologia)` | Busca case-insensitive no JSON de trilhas. Retorna lista de dicts. |
| `listar_tecnologias()` | Retorna lista ordenada e sem duplicatas de todas as tecnologias. |

O comando exibe: nível, módulos, XP total, badges, lives ao vivo e promoções ativas. Gera um plano de estudos detalhado com o número exato de módulos da trilha.

### /desafio — Desafio de Código

| Função Python | O que faz |
|---|---|
| `validar_nivel(nivel)` | Aceita: Iniciante, Intermediário, Avançado (case-insensitive). |
| `calcular_xp_desafio(nivel, seed)` | XP aleatório na faixa do nível. Seed opcional para testes determinísticos. |
| `gerar_desafio(tecnologia, nivel)` | Valida parâmetros, busca trilha, retorna dict completo do desafio. |

XP por nível: Iniciante 100–300 · Intermediário 300–600 · Avançado 600–1200. Tempo estimado incluído no retorno.

### /certificado — Emissão de Certificado

| Função Python | O que faz |
|---|---|
| `gerar_certificado(nome_aluno, tecnologia)` | Monta dict com todos os campos do certificado. |
| `renderizar_certificado_md(cert)` | Converte dict em Markdown formatado e pronto para salvar. |
| `_gerar_codigo_certificado(trail_id)` | Código único no formato `DIO-{id}-{ano}-{6chars}`. |

O certificado inclui: nome, trilha, tecnologia, nível, módulos, XP, data, código único e badges conquistadas.

---

## 4. Prompts Usados com o Bob — Catálogo Completo

> Estes são os prompts reais usados durante o desenvolvimento do projeto. Cada um mostra como instruir o Bob de forma precisa para obter exatamente o resultado desejado.

### Fase 1 — Planejamento e estruturação

**Prompt 1 — Estrutura do projeto**
```
Crie a estrutura de pastas e arquivos para o projeto DIO Explorer com as
funcionalidades /trilha, /desafio e /certificado. Use Python puro, sem frameworks web.
A lógica de negócio deve ficar separada dos comandos Bob em um módulo testável.
```

**Prompt 2 — Dados de trilhas**
```
Crie um arquivo JSON com pelo menos 20 trilhas DIO realistas. Cada trilha deve ter:
id, nome, home (URL), tecnologia, nivel, modulos, xp_total, badges (lista),
promocoes (ativa, desconto_percent, validade), vitalicio e lives_ao_vivo.
Cubra tecnologias populares: Python, Java, React, AWS, Docker, Kubernetes, etc.
```

### Fase 2 — Módulo de negócio (dio_explorer.py)

**Prompt 3 — Implementação da lógica Python**
```
Implemente o módulo dio_explorer.py com as funções:
buscar_trilhas(tecnologia), listar_tecnologias(), validar_nivel(nivel),
calcular_xp_desafio(nivel, seed=None), gerar_desafio(tecnologia, nivel),
gerar_certificado(nome_aluno, tecnologia) e renderizar_certificado_md(cert).
A busca deve ser case-insensitive. O XP deve ser aleatório dentro da faixa do nível.
O código do certificado deve ter o formato DIO-{trail_id}-{ano}-{6 chars alfanuméricos maiúsculos}.
```

### Fase 3 — Testes unitários

**Prompt 4 — Suite de testes completa**
```
Crie uma suite completa de testes unitários com pytest para os três módulos:
test_trilha.py, test_desafio.py e test_certificado.py. Use classes de teste para
organizar os cenários. Cubra: casos de sucesso, casos de erro (ValueError),
entradas inválidas, case-insensitive, campos obrigatórios.
A cobertura mínima deve ser 70%. Inclua um teste de integração ponta a ponta
trilha→desafio→certificado.
```

**Prompt 5 — Execução e relatório de testes**
```
Execute a suite de testes com pytest e cobertura. Gere um relatório completo em
dio-explorer/docs/test_results.txt incluindo: saída do pytest, cobertura por arquivo,
resultado do fluxo completo (trilha → desafio → certificado) para o aluno "João Silva"
com tecnologia Java, e um resumo final.
```

### Fase 4 — Bob Commands e Skills

**Prompt 6 — Criação dos Bob Commands**
```
Crie três Bob commands em .bob/commands/: trilha.md, desafio.md e certificado.md.
O command /trilha deve receber uma tecnologia e exibir o plano de estudos completo lendo o JSON.
O command /desafio deve receber tecnologia e nível e gerar um desafio formatado.
O command /certificado deve receber nome e tecnologia, gerar o certificado em Markdown
e perguntar se quer salvar.
```

**Prompt 7 — Criação das Bob Skills**
```
Crie as Skills equivalentes aos commands em .bob/skills/ (trilha, desafio, certificado).
As skills devem ter user-invocable: true, disable-model-invocation: true e argument-hint correto.
O conteúdo deve ser idêntico ao dos commands para que o comportamento seja o mesmo.
```

### Fase 5 — MCP Server

**Prompt 8 — Implementação do servidor MCP**
```
Crie um servidor MCP em dio-explorer/mcp/server.py que exponha as funcionalidades
do DIO Explorer como ferramentas MCP usando a API v2 (registerTool). O servidor deve
suportar dois modos: stdio (padrão, para o Bob) e HTTP/SSE (via flag --http).
O bind HTTP deve ser sempre em 127.0.0.1, nunca em 0.0.0.0. Organize as ferramentas
em módulos separados: tools/trilha.py, tools/desafio.py, tools/certificado.py.
```

**Prompt 9 — Autenticação e segurança HTTP**
```
Implemente um middleware de autenticação em dio-explorer/mcp/auth.py usando Starlette.
Deve suportar três modos via variável DIO_AUTH_MODE: api_key (padrão), oidc (futuro),
none (apenas dev). No modo api_key, leia a chave de DIO_API_KEY e compare com
hmac.compare_digest para evitar timing attacks. Libere apenas /health sem autenticação.
Nunca logue a chave.
```

**Prompt 10 — Registro do MCP no Bob**
```
Configure o servidor MCP no Bob editando .bob/mcp.json.
O servidor deve ser registrado com o nome "dio-explorer", command python e args
apontando para dio-explorer/mcp/server.py. Use o caminho absoluto do Python instalado.
```

### Fase 6 — Git Flow e documentação

**Prompt 11 — Git Flow e README**
```
Crie um README.md completo com a estratégia de Git Flow adotada no projeto.
Inclua: tabela de branches (main, develop, homologacao, production), fluxo de trabalho
com diagrama ASCII, regras de proteção por branch, convenção de nomenclatura de branches
e fluxo de hotfix em produção.
```

**Prompt 12 — Documentação completa do projeto**
```
Gostaria que documentasse todo o projeto feito até o momento, com todos os prompts usados,
modos de uso, dicas de uso e insights para futuros profissionais que vai aprender com nosso projeto.
```

---

## 5. Skills Criadas (.bob/skills/)

As Skills são instruções reutilizáveis que o Bob carrega sob demanda. São invocáveis pelo usuário via texto natural.

| Skill | Arquivo | Argumentos | Como invocar |
|---|---|---|---|
| `trilha` | `.bob/skills/trilha/SKILL.md` | `<tecnologia>` | "use skill trilha Java" |
| `desafio` | `.bob/skills/desafio/SKILL.md` | `<tecnologia> <nivel>` | "use skill desafio Python Intermediário" |
| `certificado` | `.bob/skills/certificado/SKILL.md` | `<nome> <tecnologia>` | "use skill certificado Maria Java" |

> **Diferença entre Skill e Command:** Commands são invocados com `/nome-do-command arg1 arg2`. Skills são carregadas por texto natural e funcionam como "instruções de modo" para o Bob — úteis quando você quer que o Bob *entenda o contexto* antes de agir.

---

## 6. Commands Criados (.bob/commands/)

Os Commands são acionados com a sintaxe `/nome argumento1 argumento2` diretamente no chat do Bob.

#### Exemplos de uso:

```
/trilha Java
/trilha Python
/trilha AWS

/desafio Java Intermediário
/desafio Python Iniciante
/desafio Kubernetes Avançado

/certificado "João Silva" Java
/certificado "Maria Souza" Python
/certificado "Carlos Lima" "Apache Spark"
```

| Command | Argumento 1 | Argumento 2 | Saída |
|---|---|---|---|
| `/trilha` | tecnologia | — | Plano de estudos + badges + lives + promoção |
| `/desafio` | tecnologia | nível | Enunciado + requisitos + dicas + XP + tempo |
| `/certificado` | nome do aluno | tecnologia | Certificado Markdown + opção de salvar arquivo |

---

## 7. MCP Server

### Ferramentas expostas

| Tool MCP | Parâmetros | Retorno |
|---|---|---|
| `buscar_trilha` | `tecnologia: str` | JSON com trilhas encontradas |
| `listar_tecnologias` | — | JSON com lista de tecnologias |
| `gerar_desafio` | `tecnologia, nivel` | JSON com metadados do desafio |
| `validar_nivel` | `nivel: str` | `{"valido": true/false}` |
| `gerar_certificado` | `nome_aluno, tecnologia` | JSON com campos do certificado |
| `salvar_certificado` | `nome_aluno, tecnologia` | JSON com caminho do arquivo salvo |

### Modos de execução

```bash
# Modo stdio — Bob gerencia automaticamente via mcp.json
python dio-explorer/mcp/server.py

# Modo HTTP/SSE — acesso externo via reverse-proxy
export DIO_API_KEY="sua-chave-secreta-de-pelo-menos-32-caracteres"
python dio-explorer/mcp/server.py --http --port 8000

# Health-check (sem autenticação)
curl http://127.0.0.1:8000/health

# Chamada autenticada
curl -N -H "X-API-Key: sua-chave-secreta" http://127.0.0.1:8000/sse
```

### Registro no Bob (.bob/mcp.json)

```json
{
  "mcpServers": {
    "dio-explorer": {
      "command": "python",
      "args": ["dio-explorer/mcp/server.py"],
      "env": {}
    }
  }
}
```

---

## 8. Testes e Cobertura

| Total de testes | Passaram | Falharam | Cobertura |
|:---:|:---:|:---:|:---:|
| **82** | **82** | **0** | **100%** |

| Arquivo de teste | Testes | Cenários cobertos |
|---|:---:|---|
| `test_trilha.py` | 21 | Busca por tecnologia, case-insensitive, campos obrigatórios, tecnologia não encontrada, entradas inválidas, listar tecnologias |
| `test_desafio.py` | 29 | Validação de nível, cálculo de XP, faixas por nível, seed determinística, gerar desafio completo, campos obrigatórios, tempos estimados |
| `test_certificado.py` | 32 | Geração de certificado, formato de código, data de hoje, badges, renderização Markdown, erros, fluxo completo ponta a ponta |

#### Como executar os testes:

```bash
# Na pasta dio-explorer
python run_tests.py

# Ou diretamente com pytest + cobertura
pytest src/tests/ --cov=src --cov-report=term-missing --cov-fail-under=70
```

---

## 9. Git Flow Adotado

| Branch | Ambiente | Propósito |
|---|---|---|
| `main` | Raiz | Ponto de origem do projeto |
| `develop` | Desenvolvimento | Integração contínua de features |
| `homologacao` | QA | Validação antes de produção |
| `production` | Produção | Código estável, aprovado |

```
feature/* → develop → homologacao → production
```

**Regra de ouro:** nenhum push direto nas branches protegidas. Todo código passa por Pull Request com ao menos 1 aprovação.

#### Prefixos de branches:

```
feature/cadastro-usuario        # nova funcionalidade
fix/erro-login-oauth            # correção de bug
hotfix/seguranca-token-expirado # correção urgente em produção
docs/atualiza-fluxo-git         # documentação
chore/atualiza-dependencias     # manutenção
```

---

## 10. Segurança

> Todas as decisões de segurança seguem as diretrizes IBM Security obrigatórias aplicadas pelo Bob.

| Área | Decisão adotada |
|---|---|
| Network binding | Servidor HTTP faz bind apenas em `127.0.0.1`, nunca `0.0.0.0` |
| Secrets | API Key lida de variável de ambiente `DIO_API_KEY`, nunca hardcoded |
| Autenticação | `hmac.compare_digest` para prevenir timing attacks |
| Logging | A chave nunca é logada; logs estruturados para stderr |
| Erros | Mensagens genéricas para o cliente; detalhes apenas no log do servidor |
| Fail-secure | Modo de auth desconhecido nega por padrão com HTTP 500 |
| Health-check | Único endpoint sem autenticação — adequado para probes de k8s |
| Dependências | Versões fixas no `requirements.txt` sem vulnerabilidades críticas |

---

## 11. Dicas de Uso do Bob

### Modos do Bob

| Modo | Quando usar |
|---|---|
| **Agent** | Escrever, modificar e refatorar código. É o modo padrão para implementação. |
| **Plan** | Planejar arquitetura e estratégias antes de codificar. Sem execução de código. |
| **Ask** | Perguntas técnicas, consulta de documentação IBM, entender conceitos. |

### Dicas práticas

**Dica 1 — Seja específico nos prompts**
Em vez de "crie uma função de certificado", diga exatamente quais parâmetros, qual o formato de retorno, quais validações deve ter e qual o formato do código único. Quanto mais contexto, melhor o resultado.

**Dica 2 — Separe lógica de UI desde o início**
Mantenha a lógica de negócio em um módulo Python puro, sem dependências do Bob ou MCP. Isso permite testar com pytest e reutilizar a mesma lógica nos Commands, Skills e MCP Tools.

**Dica 3 — Peça testes junto com a implementação**
No mesmo prompt, peça a implementação e os testes correspondentes. O Bob consegue criar ambos de forma coerente em uma única resposta, garantindo que os testes testem exatamente o que foi implementado.

**Dica 4 — Use skills para prompts recorrentes**
Se você usa o mesmo conjunto de instruções frequentemente (ex.: sempre gerar um plano de estudos), transforme em uma Skill. O Bob carrega as instruções automaticamente quando invocado.

**Dica 5 — MCP para integração com outros sistemas**
Quando quiser que o Bob (ou qualquer outro cliente MCP compatível) acesse sua aplicação como uma ferramenta nativa, construa um MCP Server. O Bob invoca as tools automaticamente quando necessário.

**Dica 6 — Valide a segurança em cada etapa**
O Bob aplica as diretrizes de segurança IBM automaticamente. Se você pedir algo que viola (ex.: bind em `0.0.0.0` ou hardcode de senha), ele vai explicar o motivo e oferecer uma alternativa segura. Use isso a seu favor.

**Dica 7 — Leia os arquivos antes de editar**
Antes de pedir uma modificação, diga ao Bob para "ler o arquivo X primeiro". Isso evita que ele sobreescreva código existente que você não quer modificar.

---

## 12. Insights para Futuros Profissionais

### O que este projeto demonstra na prática

**Insight 1 — IA como pair programmer, não como substituto**
O Bob não substituiu o raciocínio do desenvolvedor — ele acelerou a execução de decisões já tomadas. A arquitetura (separar lógica de negócio, criar camadas, testar puro Python) foi uma decisão humana. O Bob implementou com qualidade e velocidade. **A habilidade de saber o que pedir é o diferencial.**

**Insight 2 — Testes são inegociáveis, mesmo com IA**
O projeto tem 82 testes com 100% de cobertura. Isso não foi "exagero" — foi a garantia de que a lógica está correta independentemente de como foi gerada. Com IA, os testes ganham importância adicional: você precisa verificar que o código gerado faz o que você pediu.

**Insight 3 — MCP é o protocolo de integração do futuro**
O Model Context Protocol (MCP) permite que qualquer cliente de IA acesse suas ferramentas de forma padronizada. Aprender a construir MCP Servers é uma habilidade valiosa: sua aplicação Python vira uma "extensão nativa" de qualquer assistente compatível.

**Insight 4 — Segurança primeiro, sempre**
As regras de segurança IBM (binding em localhost, sem hardcode de secrets, hmac para comparações seguras, fail-secure por padrão) são boas práticas universais. Aprenda-as aqui e leve para qualquer projeto. Um pequeno descuido (ex.: `0.0.0.0` em produção) pode ser catastrófico.

**Insight 5 — Git Flow protege equipes**
O fluxo `main → develop → homologacao → production` com Pull Requests obrigatórios e aprovações não é burocracia — é proteção. Nenhum código com bug vai direto para produção. Essa estrutura escala de projetos pessoais a equipes de 100 pessoas.

**Insight 6 — Camadas claras de abstração**
A separação `dio_explorer.py` (negócio puro) → `tools/` (MCP) → `commands/` (Bob) permite que cada camada evolua independentemente. Você pode trocar o Bob por outro assistente, ou trocar o transporte MCP, sem mudar uma linha da lógica de negócio. Esse padrão é aplicável em qualquer projeto.

**Insight 7 — Documentação é parte do código**
Skills, Commands e READMEs são documentação executável — o Bob os lê e executa. A mesma disciplina de escrever código limpo deve ser aplicada à documentação. Um bom README e boas instruções de comando valem tanto quanto uma boa função Python.

---

### Fluxo completo executado no projeto

| Passo | Command | Resultado |
|---|---|---|
| 1 — Consulta trilha | `/trilha Java` | Trilha: Desenvolvedor Java Completo · 12 módulos · 5800 XP |
| 2 — Gera desafio | `/desafio Java Intermediário` | Serviço de processamento bancário · 450 XP · 30–60 min |
| 3 — Emite certificado | `/certificado "Joao Silva" Java` | Código DIO-2-2026-M7ESG5 · Salvo em certificados-emitidos/ |

---

*Made with IBM Bob*
