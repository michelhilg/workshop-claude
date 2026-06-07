---
name: fechamento-nf-mensal
description: >
  Executa o processo completo de fechamento fiscal mensal: lê notas fiscais em PDF
  de fornecedores, extrai dados estruturados de cada uma, cruza com contratos (em PDF
  ou planilha Excel) e identifica inconsistências como valores divergentes, notas
  duplicadas, CNPJs incorretos e fornecedores sem contrato vigente. Gera planilha
  consolidada .xlsx e relatório de fechamento em HTML ou PDF.

  Use esta skill sempre que o usuário pedir para: analisar notas fiscais, fazer o
  fechamento do mês, conferir NFs contra contratos, auditar fornecedores, gerar
  consolidado financeiro mensal, ou qualquer variação dessas tarefas — mesmo que
  não use essas palavras exatas. Qualquer pedido envolvendo NFs + contratos +
  análise deve acionar esta skill.
---

# Skill: Fechamento de NFs Mensal

Processo completo de auditoria e consolidação de notas fiscais de fornecedores.
Desenvolvida para rodar mensalmente a partir de um conjunto de NFs em PDF + arquivo
de contratos (PDF ou xlsx).

---

## 1. Entendendo as entradas

Antes de iniciar, identificar e confirmar:

| Entrada | Formato esperado | Obrigatório |
|---|---|---|
| Notas fiscais do mês | PDFs (1 arquivo por NF) | Sim |
| Base de contratos | `.xlsx` com dados dos fornecedores, **ou** PDFs dos contratos | Sim (um dos dois) |
| Mês/ano de referência | Informado no prompt ou inferido das NFs | Sim |
| Regras específicas do projeto | CLAUDE.md do projeto | Recomendado |

Se a base de contratos vier como PDFs (não como planilha), executar o **Passo 0**
antes de prosseguir. Se já existir um `contratos_fornecedores.xlsx`, pular para o
**Passo 1**.

---

## Passo 0 — Gerar contratos_fornecedores.xlsx a partir de PDFs (se necessário)

Ler cada PDF de contrato e extrair:

- Razão social da contratada
- CNPJ da contratada
- Categoria do serviço (Contabilidade, Jurídico, Marketing, TI, etc.)
- Valor mensal contratado (R$)
- Dia de vencimento mensal
- Forma de pagamento
- Data de início e fim da vigência
- Observações relevantes (reajuste, horas incluídas, multa, etc.)

Salvar como `contratos_fornecedores.xlsx` com as colunas acima + coluna `Status Contrato`
(Ativo / Encerrado / A vencer). Usar a data de vigência para determinar o status.

---

## Passo 1 — Extrair dados de cada NF

Para cada PDF de nota fiscal, extrair os campos abaixo. Se um campo não for encontrado,
registrar como `NÃO IDENTIFICADO` — nunca inferir ou inventar valores.

### Campos obrigatórios

```
numero_nf         → Número da NF (ex: "2.847", "NFS-e 5621")
data_emissao      → Data de emissão (formato DD/MM/YYYY)
competencia       → Mês/ano de competência (ex: "Maio/2026")
cnpj_prestador    → CNPJ do prestador (14 dígitos, com ou sem máscara)
razao_prestador   → Razão social do prestador
cnpj_tomador      → CNPJ do tomador (confirmar que é o da empresa esperada)
descricao_servico → Descrição completa do serviço prestado
valor_bruto       → Valor bruto total (R$)
iss_retido        → ISS retido (R$ e alíquota %, se disponível)
irrf_retido       → IRRF retido (R$)
csll_retido       → CSLL retida (R$)
pis_cofins        → PIS/COFINS retido (R$)
valor_liquido     → Valor líquido a pagar (R$)
codigo_verificacao → Código de autenticidade da NF (se presente)
nome_arquivo      → Nome do arquivo PDF de origem
```

### Validações automáticas por NF

Executar estas checagens em cada NF e registrar resultado (`OK` ou descrição do problema):

- **CNPJ formato**: 14 dígitos numéricos — flag se diferente
- **Tomador correto**: CNPJ do tomador bate com o da empresa contratante — flag se diferente
- **Valor líquido**: deve ser igual a `valor_bruto - (iss + irrf + csll + pis_cofins)` com tolerância de R$ 0,05 — flag se divergir
- **ISS alíquota**: deve estar entre 2% e 5% — flag se fora desse range
- **Competência**: mês/ano da competência deve ser compatível com o período de fechamento

---

## Passo 2 — Cruzamento NFs × Contratos

Para cada NF extraída, localizar o contrato correspondente na planilha `contratos_fornecedores.xlsx`
usando o **CNPJ do prestador** como chave primária.

### Regras de cruzamento

| Situação | O que fazer |
|---|---|
| CNPJ encontrado + valor OK | Status = `✅ OK` |
| CNPJ encontrado + valor diverge > 2% | Status = `⚠️ DIVERGÊNCIA` — calcular diferença em R$ e % |
| Mesmo CNPJ + mesma competência + mesmo valor em 2 NFs | Status = `🔁 DUPLICATA` — sinalizar ambas |
| CNPJ da NF não encontrado na base de contratos | Status = `❌ SEM CONTRATO` — pode ser fornecedor novo ou erro |
| Contrato ativo mas sem NF no mês | Status = `📭 NF AUSENTE` — listar no relatório separadamente |
| CNPJ com dígito verificador inválido | Status = `🚫 CNPJ INVÁLIDO` |

### Sobre divergências de valor

Antes de marcar como divergência, verificar se há **contexto adicional** disponível
(emails lidos, notas no CLAUDE.md, observações no contrato) que justifique a diferença.

Exemplos de contexto que reclassificam a divergência:
- "Reajuste pontual aprovado em reunião" → mudar status para `✅ REAJUSTE APROVADO`
- "NF corrigida substitui NF anterior" → marcar NF original como `🔁 SUBSTITUÍDA` e manter a nova como `✅ OK`
- "Cobrança extra de serviço adicional aprovado" → `✅ ADICIONAL APROVADO`

Registrar sempre a fonte do contexto (ex: "Email de 28/05/2026 – Mariana Costa").

---

## Passo 3 — Consolidado xlsx

Gerar arquivo `consolidado_[MMM][YY].xlsx` com as seguintes abas:

### Aba 1: `Consolidado`

Uma linha por NF processada, com as colunas:

```
fornecedor | cnpj | numero_nf | data_emissao | competencia |
valor_bruto | iss | irrf | csll | pis_cofins | valor_liquido |
valor_contratual | diferenca_r$ | diferenca_% | status | observacao
```

Formatação da coluna `status`:
- `✅ OK` → fundo verde claro (#EAF3DE)
- `⚠️ DIVERGÊNCIA` → fundo amarelo (#FAEEDA)
- `🔁 DUPLICATA` ou `🔁 SUBSTITUÍDA` → fundo laranja claro (#FDEBD0)
- `❌ SEM CONTRATO` ou `🚫 CNPJ INVÁLIDO` → fundo vermelho claro (#FCEBEB)
- `✅ REAJUSTE APROVADO` / `✅ ADICIONAL APROVADO` → fundo verde (#EAF3DE)

### Aba 2: `Alertas`

Apenas as NFs com status diferente de `✅ OK`, com coluna adicional `Ação necessária`
descrevendo o que o responsável precisa fazer.

### Aba 3: `NFs Ausentes`

Contratos ativos para os quais não chegou NF no mês. Colunas: fornecedor, CNPJ,
valor esperado, dia de vencimento, contato do fornecedor (se disponível).

### Aba 4: `Resumo`

Totais do mês:
- Total de NFs recebidas
- Total de NFs com status OK
- Total de divergências (quantidade + valor total em R$)
- Total de duplicatas
- Valor bruto total do mês
- Valor líquido total do mês
- Comparativo com mês anterior (se disponível)

---

## Passo 4 — Relatório de fechamento

Gerar `fechamento_[MMM][YY].html` (ou `.pdf` se solicitado) com:

### Estrutura do relatório

**1. Cabeçalho**
- Nome da empresa, período de fechamento, data de geração
- Número total de NFs processadas

**2. Resumo executivo** (3–5 linhas)
- O que foi processado, o que foi encontrado, o que precisa de ação

**3. Tabela principal**
- Todas as NFs com status visual (usar cores consistentes com o xlsx)
- Ordenar por: primeiro os alertas, depois os OK, por ordem alfabética de fornecedor

**4. Seção de alertas** (só se houver)
- Para cada NF com problema: descrição clara do problema + ação recomendada
- Se houver contexto de email ou outra fonte, citar a fonte

**5. NFs ausentes** (só se houver)
- Tabela com fornecedores que não mandaram NF

**6. Gráfico de distribuição por categoria**
- Barras horizontais: valor total por categoria (Contabilidade, TI, Marketing, etc.)

**7. Totais**
- Valor bruto, impostos retidos (discriminados), valor líquido total do mês

---

## Boas práticas

- **Nunca assumir** que um CNPJ parcialmente ilegível é correto — sempre flaggar
- **Nunca deletar** arquivos de NF originais — apenas gerar os arquivos de output
- **Registrar fonte** de qualquer contexto externo usado na análise (email, nota, etc.)
- **Nomear arquivos** de output sempre com o mês/ano: `consolidado_mai26.xlsx`, `fechamento_mai26.html`
- **Salvar os outputs** na pasta configurada no projeto (ex: `/output/`) ou na raiz se não especificado
- Se alguma NF estiver ilegível ou com extração incompleta, registrar no relatório e prosseguir com as demais — nunca travar o processo por causa de uma NF problemática

---

## Referência rápida: checklist de execução

```
[ ] Passo 0 – Gerar xlsx de contratos (se não existir)
[ ] Passo 1 – Extrair dados de todas as NFs
[ ] Passo 1 – Validações automáticas por NF
[ ] Passo 2 – Cruzamento NFs × contratos
[ ] Passo 2 – Verificar contexto adicional para divergências
[ ] Passo 3 – Gerar consolidado.xlsx com 4 abas
[ ] Passo 4 – Gerar relatório de fechamento
[ ] Confirmar que todos os arquivos foram salvos no destino correto
```
