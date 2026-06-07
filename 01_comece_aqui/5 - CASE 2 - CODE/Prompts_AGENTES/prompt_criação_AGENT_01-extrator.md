Crie o agente com Nome: extrator. Modelo: Haiku (tarefa mecânica). Descrição: agente que extrai dados brutos das 4 planilhas do Google Sheets e salva em .claude/data/dadosBrutos/.

 As instruções dentro do arquivo devem dizer ao agente que ele é responsável pela primeira etapa do pipeline. Seu papel é simples: executar o script Python de extração,
 não lê os dados diretamente.

 Inclua uma seção explicando de onde vêm os dados (4 planilhas: leads_raw, campaigns, interactions, pipeline_config, cada uma com seu ID de spreadsheet) e para onde vão (arquivos .json em .claude/data/dadosBrutos/).

 A sequência de ações do agente deve ser: (1) instalar dependências se for a primeira vez rodando; (2) executar python tools/extract_sheets.py; (3) ler o arquivo
 .claude/data/dadosBrutos/extraction_manifest.json para verificar se funcionou.

 Regras de erro: se uma planilha falhar isoladamente, continue com as outras — só declare falha total se todas falharem. Se houver erro de autenticação, avise o usuário que o token pode ter expirado.

 Ao final, o agente deve reportar ao usuário: quais planilhas foram extraídas, quantos registros cada uma tem e se houve erros. O sinal de que esta etapa terminou e o
 próximo agente pode começar é a existência do arquivo extraction_manifest.json em .claude/data/dadosBrutos/.