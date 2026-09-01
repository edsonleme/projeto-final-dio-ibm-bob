# DIO Explorer — MCP Server

Servidor MCP que expõe as funcionalidades do **DIO Explorer** como ferramentas
consumíveis pelo Bob (e por qualquer cliente MCP compatível).

---

## Ferramentas disponíveis

| Tool | Descrição |
|---|---|
| `buscar_trilha` | Busca trilhas DIO por tecnologia (ex.: "Java") |
| `listar_tecnologias` | Lista todas as tecnologias no catálogo |
| `gerar_desafio` | Gera metadados de um desafio por tecnologia e nível |
| `validar_nivel` | Verifica se um nível de dificuldade é válido |
| `gerar_certificado` | Gera certificado fictício de conclusão (JSON) |
| `salvar_certificado` | Gera e salva o certificado em Markdown no disco |

---

## Instalação

```bash
pip install -r dio-explorer/mcp/requirements.txt
```

---

## Modos de execução

### 1. Modo stdio (padrão — Bob spawna o processo)

```bash
python dio-explorer/mcp/server.py
```

O Bob gerencia o ciclo de vida automaticamente via `.bob/mcp.json`.

### 2. Modo HTTP/SSE (acesso externo via HTTPS)

```bash
# Variáveis obrigatórias
export DIO_API_KEY="sua-chave-secreta-longa-e-aleatoria"
export DIO_AUTH_MODE="api_key"   # padrão

# Inicia o servidor na porta 8000 (bind apenas em localhost)
python dio-explorer/mcp/server.py --http --port 8000
```

> **Importante — segurança de rede:**
> O servidor faz bind em `127.0.0.1` por padrão.
> Para expor externamente, use um **reverse-proxy com TLS** (nginx, Caddy)
> na frente. Nunca exponha diretamente em `0.0.0.0` sem TLS.

#### Exemplo de request via curl

```bash
# SSE — abre o stream de eventos
curl -N \
  -H "X-API-Key: sua-chave-secreta" \
  http://127.0.0.1:8000/sse
```

---

## Autenticação

### Modo API Key (atual)

Defina a variável de ambiente `DIO_API_KEY` com uma chave forte (>= 32 chars).
Passe-a no header de cada request:

```
X-API-Key: sua-chave-secreta
```

A comparação usa `hmac.compare_digest` para prevenir timing attacks.

### Modo SSO / OpenID Connect (futuro)

Configure `DIO_AUTH_MODE=oidc` e as variáveis abaixo quando implementado:

```
DIO_OIDC_ISSUER    = https://seu-idp.exemplo.com
DIO_OIDC_AUDIENCE  = dio-explorer-api
```

### Health-check (sem autenticação)

```bash
curl http://127.0.0.1:8000/health
```

---

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `DIO_AUTH_MODE` | `api_key` | Modo de autenticação: `api_key`, `oidc`, `none` |
| `DIO_API_KEY` | — | Chave secreta para modo `api_key` (obrigatória) |
| `DIO_MCP_HOST` | `127.0.0.1` | Host de bind do servidor HTTP |
| `DIO_MCP_PORT` | `8000` | Porta do servidor HTTP |

---

## Estrutura de arquivos

```
dio-explorer/mcp/
├── server.py          ← entrypoint principal
├── auth.py            ← middleware de autenticação HTTP
├── requirements.txt   ← dependências Python
├── README.md          ← este arquivo
└── tools/
    ├── __init__.py    ← registra todas as tools
    ├── trilha.py      ← tools: buscar_trilha, listar_tecnologias
    ├── desafio.py     ← tools: gerar_desafio, validar_nivel
    └── certificado.py ← tools: gerar_certificado, salvar_certificado
```

---

## Registro no Bob (`.bob/mcp.json`)

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

*DIO Explorer MCP Server — IBM Bob Project*
