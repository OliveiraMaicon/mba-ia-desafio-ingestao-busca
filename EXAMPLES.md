# 📚 Exemplos de Uso e Casos Práticos

## 🎯 Casos de Uso do Agente Avançado

### 1. Análise de Documentos Financeiros

**Contexto**: PDF com relatório financeiro de uma empresa

```
Pergunta 1: Qual foi o faturamento da empresa em 2023?
→ Agente busca no documento e responde

Pergunta 2: E em 2022?
→ Agente busca informação adicional

Pergunta 3: Calcule o crescimento percentual
→ Agente usa tool de calculadora: ((2023-2022)/2022)*100

Pergunta 4: Isso é um bom crescimento para o setor?
→ Agente analisa apenas com dados do documento, sem inventar

Pergunta 5: Resuma o que discutimos
→ Agente usa tool de resumo de conversação
```

### 2. Análise de Contratos

**Contexto**: PDF com contrato comercial

```
Pergunta: Quais são as cláusulas de rescisão?
→ Busca seções relevantes sobre rescisão

Pergunta: E quais as penalidades?
→ Mantém contexto e busca penalidades relacionadas

Pergunta: Em que data esse contrato foi assinado?
→ Busca data no documento

Pergunta: Quantos dias se passaram desde então?
→ Usa tool de data/hora + calculadora
```

### 3. Análise de Documentação Técnica

**Contexto**: PDF com especificações técnicas

```
Pergunta: Quais são os requisitos de hardware?
→ Busca especificações técnicas

Pergunta: O sistema suporta quanto de memória?
→ Busca informação específica

Pergunta: Se eu comprar 3 servidores com essas specs, quanto de memória total terei?
→ Extrai valor do documento + usa calculadora

Pergunta: Resuma os principais requisitos técnicos
→ Sintetiza informações técnicas encontradas
```

## 🛠️ Comandos e Tools Disponíveis

### 1. Tool: search_documents
Busca informações no documento PDF

```
Exemplos:
- "Qual o faturamento?"
- "Busque informações sobre marketing"
- "Encontre dados sobre vendas no Q4"
```

### 2. Tool: calculate
Faz cálculos matemáticos

```
Exemplos:
- "Calcule 1250000 * 0.15"
- "Quanto é (500 + 300) * 12"
- "15% de 2 milhões"
```

### 3. Tool: get_datetime
Retorna data/hora atual

```
Exemplos:
- "Que horas são?"
- "Qual a data de hoje?"
- "Me diga o dia e hora atuais"
```

### 4. Tool: summarize_conversation
Resume o histórico da conversa

```
Exemplos:
- "Resuma nossa conversa"
- "O que já discutimos?"
- "Faça um resumo dos pontos principais"
```

## 💡 Prompts Efetivos

### ✅ Boas Práticas

```
✓ "Qual o faturamento da empresa em 2023?"
  → Específico e direto

✓ "Compare o crescimento dos últimos 3 anos"
  → Clara expectativa de análise

✓ "Liste os principais riscos mencionados"
  → Objetivo bem definido

✓ "Calcule a margem líquida: (lucro / receita) * 100"
  → Fornece contexto para cálculo
```

### ❌ Evite

```
✗ "Me conte tudo sobre a empresa"
  → Muito amplo

✗ "Qual sua opinião sobre isso?"
  → Pede opinião não baseada em dados

✗ "O que acontecerá no futuro?"
  → Pede previsão não documentada

✗ "Pesquise na internet sobre..."
  → Fora do escopo do documento
```

## 🔄 Conversas com Contexto

O agente mantém memória da conversa. Exemplos:

### Exemplo 1: Análise Progressiva
```
1. "Qual foi a receita total?"
   → "A receita total foi R$ 10 milhões"

2. "E os custos?"
   → (Usa contexto) "Os custos foram R$ 7 milhões"

3. "Então o lucro foi quanto?"
   → (Usa dados anteriores) "O lucro foi R$ 3 milhões"

4. "Calcule a margem"
   → (3/10)*100 = "A margem foi 30%"
```

### Exemplo 2: Detalhamento
```
1. "Fale sobre os produtos"
   → Lista produtos do documento

2. "Qual teve melhor desempenho?"
   → Analisa e responde

3. "Por quê?"
   → (Mantém contexto do produto) Explica razões
```

## 🎭 Cenários de Demonstração

### Cenário 1: Due Diligence Financeira
```bash
# Ingira o documento financeiro
python manage.py ingest

# Inicie o agente
python manage.py agent

# Execute sequência de perguntas
1. Qual o ativo total da empresa?
2. E o passivo?
3. Calcule o patrimônio líquido (ativo - passivo)
4. Qual a relação dívida/patrimônio?
5. Resuma a situação financeira
```

### Cenário 2: Análise de Contrato
```bash
# Perguntas progressivas
1. Quem são as partes do contrato?
2. Qual o objeto do contrato?
3. Qual a vigência?
4. Quais as obrigações da parte A?
5. E da parte B?
6. Existem cláusulas de penalidade?
7. Resuma os pontos principais
```

### Cenário 3: Revisão Técnica
```bash
# Análise de especificações
1. Quais são os requisitos mínimos?
2. Quais os requisitos recomendados?
3. O sistema suporta cloud?
4. Quais são as integrações disponíveis?
5. Liste as limitações conhecidas
6. Resuma os pontos técnicos críticos
```

## 📊 Comparação: Chat vs Agent

### Usando Chat Simples (chat.py)

```
Você: Qual o faturamento?
Chat: [busca] R$ 10 milhões

Você: E o lucro?
Chat: [busca novamente, sem contexto] R$ 3 milhões

Você: Calcule a margem
Chat: Não consegue calcular (sem tool)
```

### Usando Agente (agent.py)

```
Você: Qual o faturamento?
Agent: [busca] R$ 10 milhões

Você: E o lucro?
Agent: [busca com contexto] R$ 3 milhões

Você: Calcule a margem
Agent: [usa tool + contexto] (3/10)*100 = 30%

Você: Isso é bom?
Agent: [analisa documento] Sim, está acima da média do setor mencionada (25%)

Você: Resuma
Agent: [usa tool] Discutimos: faturamento de R$10M, lucro de R$3M, 
       margem de 30%, que está acima da média do setor.
```

## 🧪 Testando o Sistema

### Teste 1: Busca Simples
```
"Qual é o nome da empresa mencionada no documento?"
→ Deve encontrar e responder corretamente
```

### Teste 2: Memória
```
1. "Qual o produto principal?"
2. "Qual o preço dele?" (usa contexto)
→ Deve manter contexto do produto da pergunta 1
```

### Teste 3: Calculadora
```
"Calcule 1234 + 5678"
→ Deve usar tool de calculadora e retornar 6912
```

### Teste 4: Data/Hora
```
"Que horas são?"
→ Deve usar tool e retornar data/hora atual
```

### Teste 5: Resumo
```
(Após várias perguntas)
"Resuma nossa conversa"
→ Deve listar os principais pontos discutidos
```

### Teste 6: Limitação (comportamento esperado)
```
"Qual a capital da França?"
→ Deve responder: "Não tenho informações necessárias para responder"
(Não deve inventar resposta)
```

## 🎯 Dicas para Máxima Eficiência

1. **Seja específico**: "Qual o faturamento em 2023?" vs "Fale sobre dinheiro"

2. **Use contexto**: Faça perguntas relacionadas em sequência

3. **Peça cálculos explicitamente**: "Calcule X + Y"

4. **Aproveite a memória**: Não repita informações já mencionadas

5. **Peça resumos**: Use "resuma" quando quiser consolidar informações

6. **Valide dados**: Faça perguntas cruzadas para confirmar informações

7. **Use comandos**: Digite 'historico' para ver conversa passada

## 🔍 Debugging de Prompts

Se não obtiver a resposta esperada:

```bash
# 1. Veja os logs
python manage.py logs

# 2. Tente reformular
Em vez de: "Me diga sobre isso"
Use: "Busque informações sobre [tópico específico]"

# 3. Divida em partes
Em vez de: "Analise tudo e calcule métricas"
Use: 
  - "Qual o valor X?"
  - "Qual o valor Y?"
  - "Calcule X/Y"

# 4. Seja explícito com tools
"Use a calculadora para..." ou "Busque no documento..."
```

## 📝 Template de Análise Completa

```
# Análise padrão de documento

1. Identificação
   - Qual o título/nome do documento?
   - Qual a data?
   - Quem são os envolvidos?

2. Dados Quantitativos
   - Quais os principais números?
   - [Se aplicável] Calcule métricas relevantes

3. Análise Qualitativa
   - Quais os pontos principais?
   - Existem riscos ou alertas?
   - Quais as conclusões?

4. Resumo
   - Resuma nossa conversa
```

---

**💡 Dica Final**: O agente é mais poderoso quando você:
- Faz perguntas específicas
- Aproveita o contexto anterior
- Usa as tools disponíveis
- Mantém conversas focadas no documento

**Experimente!** Use `python manage.py agent` e teste diferentes cenários! 🚀
