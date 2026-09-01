---
name: desafio
description: Gera um desafio de código aleatorio por nivel e tecnologia
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <tecnologia> <nivel>
---

O usuário quer um desafio de código aleatório para a tecnologia **$1** no nível **$2**.

Siga estas instruções:

1. Verifique se o nível informado é válido: `Iniciante`, `Intermediário` ou `Avançado` (ignore maiúsculas/minúsculas). Se não for válido, informe os níveis aceitos e interrompa.
2. Consulte o arquivo `dio-explorer/data/trails_dio.json` para verificar se existe alguma trilha com a tecnologia "$1". Use isso como contexto para calibrar o desafio ao ecossistema DIO.
3. Gere **um único desafio aleatório** seguindo o formato abaixo.

---

## ⚔️ Desafio de Código — {$1} | Nível: {$2}

### 📋 Enunciado

Crie um enunciado claro e objetivo para o desafio. O enunciado deve:
- Descrever um problema do mundo real ou cenário prático relacionado à tecnologia
- Ser adequado ao nível informado:
  - **Iniciante**: conceitos básicos, sintaxe, estruturas simples
  - **Intermediário**: algoritmos, manipulação de dados, padrões de projeto, APIs
  - **Avançado**: performance, arquitetura, concorrência, otimização, design patterns

### 🎯 Requisitos

Liste de 3 a 5 requisitos funcionais que a solução deve atender.

### 💡 Dicas

Forneça de 2 a 3 dicas sem entregar a solução, para orientar o raciocínio.

### 📊 Critérios de Avaliação

| Critério            | Peso |
|---------------------|------|
| Corretude           | 40%  |
| Legibilidade        | 20%  |
| Boas práticas       | 20%  |
| Tratamento de casos edge | 20% |

### ⏱️ Tempo Estimado

Informe um tempo estimado de resolução compatível com o nível:
- Iniciante: 15–30 min
- Intermediário: 30–60 min
- Avançado: 60–120 min

### 🏆 XP do Desafio

Calcule e exiba o XP que o usuário ganharia ao completar o desafio:
- Iniciante: 100–300 XP
- Intermediário: 300–600 XP
- Avançado: 600–1200 XP

(Escolha um valor aleatório dentro da faixa correspondente.)

---

Ao final, pergunte ao usuário se ele quer ver a solução de referência ou receber um novo desafio diferente.
