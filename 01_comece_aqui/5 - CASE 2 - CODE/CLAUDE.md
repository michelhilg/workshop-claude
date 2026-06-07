# AddGrowth Solutions — CRM Pipeline

## Contexto

A AddGrowth é uma empresa B2B em crescimento acelerado. Os dados do CRM estão
espalhados em 4 Google Sheets com inconsistências graves: canais escritos de
formas diferentes, etapas do funil sem padronização, leads sem responsável.

## Objetivo

Pipeline automatizado que extrai, normaliza, analisa e formata os dados para
um dashboard com um único comando.

## Arquitetura

3 agentes especializados: extrator (Haiku), analista (Sonnet), Padronizador (Haiku).
Dados transitam por .claude/data/dadosBrutos → processados → output.
Dentro da pasta de data, crie uma pasta para:
- output
- processados → devem receber os ouputs gerados pelo agente analista, após 
- dadosBrutos → devem receber somente os dados extraídos pelo nosso agente extrator