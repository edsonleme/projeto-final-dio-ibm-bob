---
description: Exibe o plano de estudos de uma trilha DIO pela tecnologia
argument-hint: <tecnologia>
---

O usuário quer visualizar o plano de estudos da trilha DIO relacionada à tecnologia: **$1**

Siga estes passos:

1. Leia o arquivo `dio-explorer/data/trails_dio.json`
2. Busque todas as trilhas cujo campo `tecnologia` contenha (busca case-insensitive) o valor "$1"
3. Se nenhuma trilha for encontrada, liste todas as tecnologias disponíveis no JSON e peça ao usuário para escolher uma

Se encontrar uma ou mais trilhas, para cada uma exiba no formato abaixo:

---

## 🎯 Trilha: {nome}

| Campo        | Detalhe                     |
|--------------|-----------------------------|
| 🏷️ Tecnologia | {tecnologia}                |
| 📊 Nível      | {nivel}                     |
| 📦 Módulos    | {modulos} módulos           |
| ⭐ XP Total   | {xp_total} XP               |
| 🔗 Acesso     | [Acessar trilha]({home})    |

### 📚 Plano de Estudos

Baseado nos dados da trilha (número de módulos, nível e tecnologia), gere um plano de estudos detalhado e realista dividido em módulos numerados. Cada módulo deve ter:
- Um título temático coerente com a tecnologia
- De 3 a 5 tópicos que seriam abordados naquele módulo
- Uma estimativa de duração em horas

O número total de módulos gerados deve ser exatamente {modulos}.

### 🏅 Badges que você vai conquistar

Liste os badges: {badges}

### 📡 Próximas Lives ao Vivo

Para cada item em `lives_ao_vivo`, exiba:
- **{titulo}** — {data} às {horario}

### 💰 Promoção

Se `promocoes.ativa` for `true`, exiba:
> 🔥 **Promoção ativa!** {desconto_percent}% de desconto — válida até {validade}

Se `promocoes.ativa` for `false`, exiba:
> Sem promoção ativa no momento.

---

Finalize com uma mensagem motivacional curta incentivando o usuário a começar a trilha.
