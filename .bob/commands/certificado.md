---
description: Gera um certificado ficticio de conclusao de trilha DIO
argument-hint: <seu-nome> <tecnologia>
---

O usuário quer gerar um certificado fictício de conclusão. Nome: **$1** | Trilha/Tecnologia: **$2**

Siga estas instruções:

1. Leia o arquivo `dio-explorer/data/trails_dio.json`
2. Busque a trilha cuja `tecnologia` contenha (case-insensitive) o valor "$2"
3. Se não encontrar, informe as tecnologias disponíveis e interrompa
4. Use os dados da trilha encontrada para preencher o certificado abaixo

Gere o certificado **em Markdown** com o seguinte layout exato:

---

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              🎓  DIGITAL INNOVATION ONE  🎓                      ║
║                      dio.me                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

# 📜 Certificado de Conclusão

---

> *A Digital Innovation One certifica que*

## $1

> *concluiu com êxito a trilha de aprendizado*

# {nome da trilha}

---

| 🏷️ Tecnologia  | {tecnologia}                        |
|----------------|-------------------------------------|
| 📊 Nível       | {nivel}                             |
| 📦 Módulos     | {modulos} módulos concluídos        |
| ⭐ XP Obtido   | {xp_total} XP                       |
| 📅 Data        | {data de hoje no formato DD/MM/AAAA}|
| 🔑 Código      | DIO-{id da trilha}-{ano atual}-{gere 6 caracteres alfanuméricos aleatórios maiúsculos} |

---

### 🏅 Badges Conquistadas

Para cada badge da trilha, exiba como: `🏅 {badge}`

---

### 💬 Mensagem de Parabenização

Escreva um parágrafo motivacional personalizado (3–4 frases) parabenizando **$1** pela conclusão da trilha **{nome da trilha}**, destacando as habilidades adquiridas na tecnologia **{tecnologia}** e incentivando os próximos passos na carreira.

---

*Certificado fictício gerado pelo DIO Explorer — IBM Bob Project*
*Verifique autenticidade em: https://www.dio.me/certificate*

---

Após exibir o certificado, pergunte ao usuário se deseja salvar o certificado como arquivo Markdown em `dio-explorer/docs/certificados-emitidos/certificado-$1.md` (substituindo espaços por hífens no nome do arquivo).

Se o usuário confirmar, salve o arquivo com exatamente o conteúdo do certificado gerado (sem o bloco de código externo, apenas o Markdown limpo).
