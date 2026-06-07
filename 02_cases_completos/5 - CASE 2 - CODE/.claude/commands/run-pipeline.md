Execute o pipeline completo de CRM da AdGrowth em sequência, rodando os 3 agentes especializados um após o outro. Pare imediatamente se qualquer etapa falhar.

## Etapa 1 — Extrator

Você é o agente **extrator**. Diretório raiz: `C:\Users\Lu
cas Xiang\Desktop\AdGrowth`.

1. Verifique se as dependências estão instaladas. Se não, rode `py -m pip install -r tools/requirements.txt`.
2. Execute `py tools/extract_sheets.py`.
3. Confirme que `.claude/data/dadosBrutos/extraction_manifest.json` foi gerado.
4. Se todas as planilhas falharem, **pare o pipeline e reporte o erro**.

Reporte: planilhas extraídas, registros por planilha, erros.

---

## Etapa 2 — Analista

Você é o agente **analista**. Pré-condição: `extraction_manifest.json` deve existir.

1. Carregue `.claude/agents/analista/config.json` (CANAL_MAP, ETAPA_MAP).
2. Leia os 4 arquivos de `.claude/data/dadosBrutos/`.
3. Construa os índices de campanhas, interações e pipeline.
4. Normalize canal e etapa de cada lead; registre inconsistências.
5. Enriqueça cada lead com os 3 índices.
6. Calcule as métricas agregadas (funil, conversão, volume mensal, won/lost, score, sentimento, objeções).
7. Salve os 4 arquivos em `.claude/data/processados/` e confirme que `analysis_manifest.json` foi gerado.
8. Se os arquivos de entrada estiverem ausentes, **pare o pipeline e reporte**.

Reporte: leads processados, taxa de normalização, inconsistências encontradas.

---

## Etapa 3 — Padronizador

Você é o agente **padronizador**. Pré-condição: `analysis_manifest.json` deve existir em `.claude/data/processados/`.

1. Execute `py tools/format_output.py`.
2. Confirme que `output_manifest.json` foi gerado em `.claude/data/output/`.
3. Leia `dashboard_summary.json` e extraia os KPIs principais.

Reporte: arquivos gerados, total de leads, valor total do pipeline, alertas operacionais.

---

## Relatório Final do Pipeline

Ao concluir as 3 etapas, exiba um relatório consolidado:

```
Pipeline AdGrowth — Concluído
══════════════════════════════════════════
Etapa 1 · Extrator      ✓  XX.XXX registros extraídos
Etapa 2 · Analista      ✓  XX.XXX leads processados (XX% normalizados)
Etapa 3 · Padronizador  ✓  9/9 arquivos gerados
──────────────────────────────────────────
Total de leads:         XX.XXX
Valor total:            R$ XX.XXX.XXX,XX
Alertas operacionais:   XX
Dados prontos para o dashboard.
══════════════════════════════════════════
```

Se qualquer etapa falhou parcialmente, liste os erros ao final do relatório.
