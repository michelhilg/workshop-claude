Crie o agente com nome: analista. Modelo: Sonnet (precisa raciocinar). Descrição: agente que normaliza os dados brutos de .claude/data/dadosBrutos/, une as 4 fontes em um modelo limpo,
 calcula métricas e gera análises de negócio, salvando os resultados em .claude/data/processados/.

 Este agente tem duas etapas internas:

 Etapa 1 (mecânica): Antes de fazer qualquer coisa, verificar se .claude/data/dadosBrutos/extraction_manifest.json existe. Se não existir, parar e avisar que o extractor precisa rodar primeiro. Depois, executar py tools/normalize_and_join.py. Este script produz 4 arquivos em .claude/data/processados/: os leads limpos e normalizados, um
 relatório de padrões suspeitos, as métricas pré-calculadas e um resumo da execução.

 Etapa 2 (raciocínio LLM): Depois que o script terminar, o agente deve ler dois arquivos compactos — aggregated_metrics.json e patterns.json, ambos em
 .claude/data/processados/ — e produzir um arquivo insights.json no mesmo diretório com análises aprofundadas em 6 dimensões:

 1. Tendências (trends): há crescimento de leads ao longo dos meses? Tem sazonalidade? Quais meses foram acima/abaixo da média?
 2. Análise de insucesso (lost_analysis): qual a taxa de perda geral e por canal? Em que etapa mais leads são perdidos? Quais objeções mais aparecem? Quais segmentos e
 vendedores têm mais perda?
 3. Análise de sucesso (won_analysis): qual canal converte mais? Qual segmento tem maior valor médio? O que diferencia os vendedores com melhor resultado? Qual o perfil
 típico de um lead ganho?
 4. Gargalos do funil (funnel_bottlenecks): entre quais etapas tem a maior queda de volume? Qual etapa concentra mais dinheiro em risco?
 5. Padrões de sentimento (sentiment_patterns): como o sentimento varia por etapa? Quais objeções aparecem nas etapas avançadas? Sentimento negativo correlaciona com
 perda?
 6. Recomendações (recommendations): entre 5 e 8 ações práticas, cada uma com: o que fazer (action), por que fazer (rationale), qual o impacto esperado (expected_impact) e
  prioridade (priority: high, medium ou low).

 Inclua o schema exato do insights.json no arquivo de definição, para que o agente saiba precisamente o formato de saída esperado.

 Ao final, o agente reporta ao usuário: os principais achados de cada dimensão (2–3 linhas por seção) e as 3 recomendações de maior prioridade.