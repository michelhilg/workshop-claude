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
Nexus/2. Financeiro/1. Notas Fiscais/2026/        → Notas Fiscais de 2026 (Google Drive)
/contratos/                     → Contratos em PDF dos fornecedores (local)
/output/                        → Saída gerada pelo Cowork

---

## Skills Disponíveis

- **`fechamento_nf_mensal`** → Extrai dados estruturados de uma NF: fornecedor, CNPJ, valor, competência, descrição do serviço, impostos


> Se alguma skill não estiver disponível, pare e informe antes de prosseguir.

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
