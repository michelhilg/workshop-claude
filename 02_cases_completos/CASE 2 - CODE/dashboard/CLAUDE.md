# AdGrowth Dashboard

## Objetivo
Dashboard React que consome os dados tratados pelo sistema agêntico AdGrowth CRM.
Visualiza métricas de funil, campanhas, vendedores, objeções e qualidade de dados.

## Stack
- **Vite + React + TypeScript**
- **Tailwind CSS v3** (via PostCSS)
- **Recharts** (gráficos)
- **React Router v6** (navegação)
- **Lucide React** (ícones)
- Sem backend — dados servidos como assets estáticos via `public/data/`

## Fonte de Dados
Os arquivos JSON consumidos pelo dashboard vivem em `public/data/` e são gerados
pelo pipeline agêntico localizado em `../.claude/data/processados/`.

Para sincronizar os dados mais recentes do pipeline, execute:
```bash
bash scripts/sync-data.sh
```

Arquivos consumidos:
- `public/data/aggregated_metrics.json` — métricas pré-agregadas (13KB)
- `public/data/analysis_manifest.json` — status e estatísticas do pipeline

O arquivo `leads_clean.json` (~36MB) NÃO é carregado por padrão — está disponível
em `../.claude/data/processados/` para drill-down futuro se necessário.

## Como rodar
```bash
npm install
bash scripts/sync-data.sh   # sincroniza dados do pipeline
npm run dev                 # inicia em localhost:5173
```

## Estrutura de Páginas
| Rota | Página | Dados principais |
|---|---|---|
| `/` | Overview | total_leads, monthly_volume, won/lost por canal |
| `/funnel` | Funil de Vendas | funnel_summary, conversion_rates |
| `/campaigns` | Campanhas | won/lost por canal e segmento |
| `/reps` | Vendedores | won/lost por vendedor |
| `/objections` | Objeções | por_objecao (won vs lost), objecoes_by_stage |
| `/quality` | Qualidade de Dados | normalization_stats, score_distribution, sentiment_by_stage |

## Estrutura de Pastas
```
src/
├── types/crm.ts          # interfaces TypeScript dos dados
├── hooks/useData.ts      # carrega e expõe os JSONs tipados
├── components/
│   ├── layout/           # Layout, Sidebar
│   └── cards/            # KpiCard
└── pages/                # uma página por rota
```

## Convenções
- Formatação monetária: `Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })`
- Formatação numérica: `Intl.NumberFormat('pt-BR').format(n)`
- Percentuais: `.toFixed(1) + '%'`
- Cores dos gráficos: azul=#3B82F6, verde=#22C55E, vermelho=#EF4444, âmbar=#F59E0B
