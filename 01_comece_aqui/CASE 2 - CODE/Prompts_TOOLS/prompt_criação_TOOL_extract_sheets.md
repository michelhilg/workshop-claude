Crie um script Python chamado extract_sheets.py dentro da pasta tools/.

Caso necessário, instale o python e as dependencias necessárias. 

 Ele precisa se autenticar na Google Sheets API via service account (arquivo JSON de credenciais). Deve ler 4 planilhas distintas do Google Sheets — leads_raw, campaigns,
 interactions, pipeline_config — cada uma com seu próprio spreadsheet_id e aba.

 Para cada planilha, extraia todas as linhas, use a primeira linha como cabeçalho e converta o resultado em uma lista de dicionários JSON. Adicione dois campos de
 metadados em cada registro: _source_sheet (nome da fonte) e _extracted_at (timestamp ISO 8601 do momento da extração).

 Se o nome da aba configurada não existir na planilha, tente detectar automaticamente a primeira aba disponível antes de falhar.

Ele precisa se autenticar na Google Sheets API via service account (arquivo JSON de credenciais). Deve ler 4 planilhas distintas do Google Sheets — cada uma com seu
próprio spreadsheet_id e aba:

 | Nome            | Spreadsheet ID                               |
 |-----------------|----------------------------------------------|
 | leads_raw       | 1nLtBkCsFcidxVau7GNrySfAe8YAbp8NjvYWBjRWlAe4 |
 | campaigns       | 1XVTNK0bQprmQAjZUHceAOlcqrYvOQQ7-i-T6IrYUMRU |
 | interactions    | 1QPKIquhQJ_fYfSRmwTBmr0GqUh2e4uKDAxiheEXgBNk |
 | pipeline_config | 1GUFl32bAqOsxgXsjOrSQuTL2tQlj6Eg1rPAyauhwXTk |

 Para cada planilha, extraia todas as linhas, use a primeira linha como cabeçalho e converta o resultado em uma lista de dicionários JSON. Adicione dois campos de
 metadados em cada registro: _source_sheet (nome da fonte) e _extracted_at (timestamp ISO 8601 do momento da extração).
 Se o nome da aba configurada não existir na planilha, tente detectar automaticamente a primeira aba disponível antes de falhar.

 Salve cada planilha como um arquivo .json separado em .claude/data/dadosBrutos/ (ex: leads_raw.json). Ao final, gere também um extraction_manifest.json com o status de
 cada fonte (sucesso/falha), contagem de registros e o timestamp da extração.

 As configurações de IDs, nomes de abas e caminho do arquivo de credenciais devem vir de .claude/agents/extrator/config.json. Dependências: google-auth,
 google-auth-httplib2, google-api-python-client.