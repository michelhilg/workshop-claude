Crie o agente com nome: padronizador. Modelo: Haiku (tarefa mecânica). Descrição: agente que lê os dados de .claude/data/processados/ e gera os arquivos finais prontos para o dashboard.

As instruções devem dizer que este é o último agente do pipeline. Seu papel é executar o script Python de formatação, não reformatar nada manualmente.

 A sequência de ações: (1) verificar se .claude/data/processados/analysis_manifest.json existe — se não existir, parar e avisar que o analyzer precisa rodar primeiro; (2)
 executar python tools/format_output.py; (3) ler .claude/data/output/output_manifest.json para confirmar quais arquivos foram gerados.

 Inclua uma tabela listando os 9 arquivos que o script produz em .claude/data/output/ e o que cada um contém: resumo do dashboard com KPIs, visão do pipeline por etapa,
tabela completa de leads, performance por canal, performance por campanha, performance por vendedor, alertas operacionais, relatório de qualidade de dados e recomendações
priorizadas.

Ao final, o agente reporta: quantos arquivos foram gerados, os números-chave do dashboard_summary.json (total de leads, valor total, quantidade de alertas) e eventuais
erros.