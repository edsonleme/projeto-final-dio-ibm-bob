# projeto-final-dio-ibm-bob

Projeto final do bootcamp **DIO + IBM** desenvolvido com o assistente **Bob**.

---

## 🌿 Estratégia de Branches (Git Flow)

Este projeto adota um fluxo de branches estruturado para garantir que código com bugs ou não validado nunca chegue ao ambiente de produção.

### Branches principais

| Branch | Ambiente | Propósito |
|---|---|---|
| `main` | — | Branch raiz / ponto de origem do projeto |
| `develop` | Desenvolvimento | Integração contínua de features e correções |
| `homologacao` | Homologação (QA) | Validação e testes antes de ir para produção |
| `production` | Produção | Código estável, aprovado e em execução |

---

### Fluxo de trabalho

```
feature/* ou fix/*
       │
       ▼
    develop   ──────►   homologacao   ──────►   production
  (dev / CI)           (QA / testes)           (estável / prod)
```

1. **Desenvolvimento** — todo trabalho começa em uma branch derivada de `develop`:
   ```bash
   git checkout develop
   git checkout -b feature/minha-feature
   # ... commits ...
   git push origin feature/minha-feature
   # Abrir Pull Request → develop
   ```

2. **Promoção para Homologação** — após revisão e aprovação do PR em `develop`, abre-se um PR de `develop` → `homologacao` para validação em ambiente de testes.

3. **Promoção para Produção** — após validação em homologação, abre-se um PR de `homologacao` → `production`. Requer ao menos **1 aprovação** antes do merge.

---

### Regras de proteção de branches

As branches `develop`, `homologacao` e `production` possuem as seguintes proteções configuradas no GitHub:

| Regra | `develop` | `homologacao` | `production` |
|---|:---:|:---:|:---:|
| Require pull request before merge | ✅ | ✅ | ✅ |
| Required approving reviews | 1 | 1 | 1 |
| Dismiss stale reviews | ✅ | ✅ | ✅ |
| Require status checks to pass | ✅ | ✅ | ✅ |
| Restrict who can push directly | ✅ | ✅ | ✅ |

> **Nenhum push direto é permitido** nas branches protegidas — todo código deve passar por Pull Request.

---

### Convenção de nomenclatura de branches

| Prefixo | Uso |
|---|---|
| `feature/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `hotfix/` | Correção urgente em produção |
| `chore/` | Tarefas de manutenção (deps, configs) |
| `docs/` | Atualização de documentação |

**Exemplos:**
```
feature/cadastro-usuario
fix/erro-login-oauth
hotfix/seguranca-token-expirado
docs/atualiza-fluxo-git
```

---

### Hotfix em produção

Em caso de bug crítico em produção, o hotfix deve seguir o fluxo:

```
production
    │
    ├──► hotfix/descricao-do-problema
    │         │
    │         ▼
    │    (PR → production)
    │
    └──► (cherry-pick ou merge → homologacao → develop)
```

---

## Como começar

```bash
# Clone o repositório
git clone https://github.com/edsonleme/projeto-final-dio-ibm-bob.git
cd projeto-final-dio-ibm-bob

# Trabalhe sempre a partir da branch develop
git checkout develop
git checkout -b feature/nome-da-sua-feature
```

---

*Projeto Final — DIO + IBM Bootcamp*
