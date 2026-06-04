# CLAUDE.md — Projeto: Fechamento Fiscal Nexus

## Contexto do Projeto

**Cliente:** Nexus Consultoria em Gestão Empresarial  
**Domínio:** Gestão fiscal e financeira de fornecedores  
**Objetivo do projeto:** Automatizar o processo de fechamento fiscal mensal, cruzando Notas Fiscais recebidas com contratos vigentes e comunicações por email, gerando relatórios consolidados para auditoria interna.

A Nexus possui uma carteira de fornecedores recorrentes com contratos formalizados. Todo mês, o time financeiro precisa:
1. Validar se os valores das NFs batem com o que foi contratado
2. Identificar divergências (cobranças acima do contrato)
3. Checar se alguma divergência foi previamente aprovada via email (reajustes, exceções pontuais)
4. Gerar um relatório consolidado para o gestor financeiro

---

## Estrutura de Pastas

### Local (pasta do projeto)
```
/contratos/          → 10 PDFs de contratos dos fornecedores
/output/             → Saída gerada pelo Cowork
  contratos_fornecedores.xlsx   → Base consolidada de contratos (gerada em Jun/2026 — reutilizar)
  consolidado_[MMM][AA].xlsx    → Consolidado mensal de NFs
  fechamento_[MMM][AA].pdf      → Relatório executivo mensal
  NFs_[MMM][AA]/                → NFs do mês baixadas do Drive (índice + arquivos)
```

### Google Drive
```
Nexus/2. Financeiro/1. Notas Fiscais/2026/   → pasta raiz de NFs 2026
  1. Janeiro/ … 5. Maio/ …                   → uma subpasta por mês
```
- **ID da pasta "1. Notas Fiscais":** `1XmgWHle4pydsuN0W3SRT71Y1lGIKVnHx`
- **ID da pasta "2026":** `11l0_OIqepK9xLPFrvOCktEmSfR4Vqs3A`
- Cada mês está no formato `N. NomeMês` (ex.: `5. Maio`, ID: `1ROcw98j3H23apBPbiblEIH-jIMFF9W4l`)

### Gmail
- Conta do analista financeiro: `lucasmafamg@gmail.com`
- Buscar por: nome do fornecedor + termos como `reajuste`, `aprovação`, `exceção`, `novo valor`, `aditivo`, `NF corrigida`

---

## Skills Disponíveis

- **`fechamento-nf-mensal`** → Processo completo: extrai NFs, cruza com contratos, gera Excel (4 abas) e PDF executivo
- **`xlsx`** → Criação e edição de planilhas Excel
- **`pdf`** → Criação e manipulação de PDFs

> Se alguma skill não estiver disponível, pare e informe antes de prosseguir.

---

## Connectors Disponíveis

- **Google Drive** — para acessar NFs na pasta `Nexus/2. Financeiro/1. Notas Fiscais/2026/`
- **Gmail** — para buscar emails de aprovação/reajuste no período do fechamento

---

## Base de Contratos

O arquivo `output/contratos_fornecedores.xlsx` já foi gerado em Junho/2026 com os 10 contratos ativos.  
**Não é necessário reprocessar os PDFs de contratos a cada mês** — apenas verificar se houve alterações ou novos contratos.

### Fornecedores cadastrados (referência rápida)
| Fornecedor | CNPJ | Categoria | Valor Mensal | Vencimento | Vigência |
|---|---|---|---|---|---|
| BenefíciosMais Gestão de RH Ltda | 89.012.345/0001-08 | RH / Benefícios | R$ 6.200,00 | Dia 25 | 01/01–31/12/2026 |
| CloudHost Brasil Hospedagem Ltda | 56.789.012/0001-05 | TI / Hospedagem | R$ 890,00 | Dia 01 | 01/01–31/12/2026 |
| ContabilPro Assessoria Contábil Ltda | 12.345.678/0001-01 | Contabilidade | R$ 2.800,00 | Dia 10 | 01/01–31/12/2026 |
| DigitalBoost Comunicação e Marketing Ltda | 34.567.890/0001-03 | Marketing | R$ 3.800,00 | Dia 05 | 01/01–31/12/2026 |
| LimpaBem Serviços de Limpeza Ltda | 67.890.123/0001-06 | Limpeza | R$ 1.600,00 | Dia 10 | 01/02/2026–31/01/2027 |
| LogiExpress Transportes e Courier Ltda | 01.234.567/0001-10 | Logística | R$ 980,00 | Dia 20 | 01/03/2026–28/02/2027 |
| SeguraTech Seguros Empresariais S.A. | 90.123.456/0001-09 | Seguros | R$ 1.450,00 | Dia 15 | **01/06/2026**–31/05/2027 |
| Silva & Advogados Associados | 23.456.789/0001-02 | Jurídico | R$ 3.500,00 | Dia 15 | 01/03/2026–28/02/2027 |
| TechSupport Soluções em TI Ltda | 45.678.901/0001-04 | TI / Suporte | R$ 2.200,00 | Dia 20 | 01/04/2026–31/03/2027 |
| WorkSpace Coworking e Escritórios Ltda | 78.901.234/0001-07 | Escritório | R$ 4.500,00 | Dia 05 | 01/01–31/12/2026 |

**CNPJ da Nexus (tomador):** 11.222.333/0001-44

---

## Regras de Negócio

### Classificação de NFs no cruzamento:
| Situação | Classificação |
|---|---|
| Valor da NF = valor do contrato (±2%) | `OK` |
| Valor da NF > contrato, sem justificativa | `DIVERGÊNCIA` |
| Valor da NF > contrato, com email de aprovação encontrado | `REAJUSTE APROVADO` |
| NF sem contrato correspondente | `SEM CONTRATO` |
| Contrato sem NF no mês | `NF AUSENTE` |

### Identificação de reajuste via email:
- Considere um email como justificativa válida se mencionar explicitamente: nome do fornecedor + algum dos termos: reajuste, aprovação, exceção, novo valor, aditivo, ajuste de contrato
- Extraia do email: data, remetente, trecho relevante — isso vai para a coluna "Observação" na planilha

---

## Regras de Segurança

1. **Nunca sobrescrever arquivos existentes em `/output/`** sem perguntar. Se o arquivo já existir, perguntar: *"O arquivo X já existe. Deseja sobrescrever ou salvar como nova versão?"*
2. **Nunca deletar NFs, contratos ou emails** — leitura apenas, jamais modificar a origem
3. **Nunca assumir uma classificação ambígua** — se um fornecedor aparecer com nome ligeiramente diferente no contrato e na NF, perguntar antes de vincular
4. **Se uma etapa falhar**, não avançar para a próxima. Informar o erro, o que foi tentado e o que precisa de decisão
5. **Dados sensíveis**: este projeto lida com informações financeiras e contratuais da Nexus. Não expor valores, CNPJ ou nomes de fornecedores fora do escopo deste projeto
