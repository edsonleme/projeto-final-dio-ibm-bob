## ⚔️ Desafio de Código — Java | Nível: Intermediário

> Gerado pelo DIO Explorer — IBM Bob Project
> Trilha de referência: **Desenvolvedor Java Completo** (DIO)

---

### 📋 Enunciado

Você trabalha em uma fintech e precisa implementar um **serviço de processamento de transações bancárias** utilizando Java. O sistema deve receber uma lista de transações (transferências entre contas), validar cada uma delas e retornar um relatório consolidado com os saldos finais de cada conta.

Cada transação é representada por:
- `contaOrigem` (String)
- `contaDestino` (String)
- `valor` (double)

O sistema deve rejeitar transações com valor negativo ou zero e transações onde a conta de origem não possui saldo suficiente. As contas são inicializadas com saldo de R$ 1.000,00 por padrão.

---

### 🎯 Requisitos

1. Criar a classe `Transacao` com os atributos `contaOrigem`, `contaDestino` e `valor`.
2. Criar a classe `ProcessadorTransacoes` com o método `processar(List<Transacao> transacoes)` que retorna um `Map<String, Double>` com os saldos finais de cada conta.
3. Rejeitar (e registrar em log) transações inválidas: valor ≤ 0 ou saldo insuficiente na conta de origem.
4. Utilizar **Stream API** para filtrar transações válidas antes de processá-las.
5. Escrever ao menos **3 testes unitários** com JUnit 5 cobrindo: transação válida, saldo insuficiente e valor negativo.

---

### 💡 Dicas

- Use `HashMap<String, Double>` para armazenar os saldos e inicialize todas as contas encontradas nas transações com R$ 1.000,00.
- A Stream API com `filter()` é ideal para separar transações válidas de inválidas antes do loop de processamento.
- Para o logging, `java.util.logging.Logger` é suficiente — não é necessário adicionar dependências externas.

---

### 📊 Critérios de Avaliação

| Critério                    | Peso |
|-----------------------------|------|
| Corretude                   | 40%  |
| Legibilidade                | 20%  |
| Boas práticas               | 20%  |
| Tratamento de casos edge    | 20%  |

---

### ⏱️ Tempo Estimado

**30–60 minutos** (Nível Intermediário)

---

### 🏆 XP do Desafio

**450 XP** ao completar este desafio!

---

*Desafio fictício gerado pelo DIO Explorer — IBM Bob Project*
*Trilha: Desenvolvedor Java Completo | https://www.dio.me/trilhas/desenvolvedor-java-completo*
