# Configurando Google Service Account para o Workshop

> **Contexto:** Este guia cria as credenciais que o script `extract_sheets.py` usa para acessar planilhas no Google Drive de forma automatizada — sem login manual, sem browser, sem intervenção humana.

---

## O que é uma Service Account?

Uma **Service Account** é uma conta do Google criada para aplicações (não para pessoas). Em vez de logar com usuário e senha, o script autentica com um arquivo `.json` de credenciais. É a forma correta de acessar Google APIs em automações.

No `extract_sheets.py`, isso acontece aqui:

```python
from google.oauth2 import service_account

def get_credentials(service_account_file: str):
    return service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
```

O `service_account_file` aponta para o JSON que vamos baixar neste guia. O `SCOPES` define que só queremos **leitura** de planilhas:

```python
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
```

---

## Pré-requisitos

- Conta Google (pessoal ou Google Workspace)
- Acesso ao [Google Cloud Console](https://console.cloud.google.com)
- Uma pasta no Google Drive com as planilhas que o script vai ler

---

## Passo 1 — Criar (ou selecionar) um Projeto no Google Cloud

1. Acesse [https://console.cloud.google.com](https://console.cloud.google.com)
2. No topo da página, clique no **seletor de projetos** (ao lado do logo Google Cloud)
3. Clique em **"Novo projeto"**
4. Preencha:
   - **Nome do projeto:** `workshop-claude-sem-frescura` (ou qualquer nome)
   - **Organização:** deixe como está
5. Clique em **"Criar"**
6. Aguarde a criação e certifique-se de que o projeto novo está selecionado no topo

> ⚠️ Todos os passos seguintes devem ser feitos dentro deste projeto.

---

## Passo 2 — Habilitar a Google Sheets API

1. No menu lateral esquerdo, vá em **"APIs e serviços" → "Biblioteca"**
2. Na barra de busca, digite: `Google Sheets API`
3. Clique no resultado **"Google Sheets API"**
4. Clique no botão **"Ativar"**
5. Aguarde a ativação (leva alguns segundos)

> **Por que isso é necessário?** O Cloud Console não permite acesso a APIs por padrão — cada API precisa ser explicitamente habilitada no projeto.

---

## Passo 3 — Criar a Service Account

1. No menu lateral, vá em **"APIs e serviços" → "Credenciais"**
2. Clique em **"+ Criar credenciais"** (topo da página)
3. Selecione **"Conta de serviço"**
4. Preencha os campos:
   - **Nome da conta de serviço:** `leitor-planilhas` (ou similar)
   - **ID da conta:** será preenchido automaticamente (ex: `leitor-planilhas@seu-projeto.iam.gserviceaccount.com`)
   - **Descrição:** `Leitura de planilhas para pipeline do workshop`
5. Clique em **"Criar e continuar"**
6. Na etapa **"Conceder acesso ao projeto"**: pode pular clicando em **"Continuar"**
7. Na etapa **"Conceder acesso aos usuários"**: pode pular clicando em **"Concluído"**

Você verá a service account listada na seção **"Contas de serviço"** da página de Credenciais.

---

## Passo 4 — Baixar o arquivo JSON de credenciais

1. Na lista de contas de serviço, clique no **e-mail** da conta que você criou
2. Acesse a aba **"Chaves"**
3. Clique em **"Adicionar chave" → "Criar nova chave"**
4. Selecione o formato **JSON**
5. Clique em **"Criar"**

O arquivo será baixado automaticamente. Ele terá um nome parecido com:
```
seu-projeto-a1b2c3d4e5f6.json
```

> 🔐 **Segurança:** Este arquivo é equivalente a uma senha. Nunca commite ele no git. Adicione ao `.gitignore`:
> ```
> *.json
> credentials/
> .claude/agents/extractor/credentials/
> ```

---

## Passo 5 — Posicionar o arquivo no projeto

No script `extract_sheets.py`, o caminho das credenciais vem do `config.json`:

```python
BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / ".claude" / "agents" / "extractor" / "config.json"
```

E dentro do `config.json`, a chave `service_account_file` aponta para o JSON:

```json
{
  "service_account_file": "credentials/service-account.json",
  "output_dir": ".claude/data/raw",
  "sheets": {
    "crm_leads": {
      "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
      "sheet_name": "Sheet1"
    }
  }
}
```

Mova o arquivo baixado para o caminho definido em `service_account_file`, relativo à `BASE_DIR`:

```
projeto/
├── .claude/
│   ├── agents/
│   │   └── extractor/
│   │       └── config.json
│   └── data/
│       └── raw/          ← arquivos JSON extraídos vão aqui
├── credentials/
│   └── service-account.json   ← coloque o arquivo aqui
└── tools/
    └── extract_sheets.py
```

---

## Passo 6 — Dar acesso à Service Account na pasta do Drive

Este é o passo mais importante e frequentemente esquecido. A service account é uma "pessoa" do Google — ela precisa de permissão explícita para ler seus arquivos.

1. Abra o [Google Drive](https://drive.google.com)
2. Navegue até a **pasta** que contém as planilhas
3. Clique com o botão direito na pasta → **"Compartilhar"**
4. No campo de e-mail, cole o endereço da service account:
   ```
   leitor-planilhas@seu-projeto.iam.gserviceaccount.com
   ```
   > O e-mail está no arquivo JSON baixado, no campo `"client_email"`
5. Defina a permissão como **"Leitor"** (apenas leitura)
6. **Desmarque** "Notificar pessoas" (é uma conta de serviço, não receberá e-mail)
7. Clique em **"Compartilhar"**

> ✅ Pronto. A service account agora consegue listar e ler todas as planilhas dentro dessa pasta.

---

## Passo 7 — Obter o `spreadsheet_id` das planilhas

O script precisa do ID de cada planilha para acessá-la. O ID está na URL do Google Sheets:

```
https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms/edit
                                       ↑_________________________________________↑
                                                    este é o spreadsheet_id
```

Copie esse ID e adicione ao `config.json` na seção `sheets`.

---

## Verificando se tudo está funcionando

Com as dependências instaladas (`pip install google-auth google-api-python-client`), execute:

```bash
python tools/extract_sheets.py
```

**Saída esperada:**
```
[OK] crm_leads: 87 registros → crm_leads.json

Extração concluída: 1 sheet(s) OK, 0 erro(s).
```

**Erro mais comum:**
```
HttpError 403: The caller does not have permission
```
→ A service account ainda não recebeu acesso à pasta. Refaça o Passo 6.

```
HttpError 400: Unable to parse range
```
→ O nome da aba no `config.json` está diferente do nome real na planilha. O script detecta isso e tenta automaticamente a primeira aba disponível:
```python
if e.resp.status == 400:
    available = list_sheet_names(service, spreadsheet_id)
    print(f"  [AVISO] Aba '{tab_name}' não encontrada. Tentando '{available[0]}'")
```

---

## Conexão completa com o script

```
config.json
    ↓ service_account_file
credentials/service-account.json
    ↓ get_credentials()
google.oauth2.service_account.Credentials
    ↓ build("sheets", "v4", credentials=creds)
Google Sheets API
    ↓ spreadsheets().values().get(spreadsheetId=..., range=...)
Dados brutos
    ↓ rows_to_records()
.claude/data/raw/{sheet_name}.json
    ↓ extraction_manifest.json
Pipeline de análise (agentes subsequentes)
```

---

## Resumo dos arquivos sensíveis (nunca commitar)

```gitignore
# Credenciais Google
credentials/
*.json

# Dados extraídos (podem conter dados reais)
.claude/data/raw/
```

---

*Guia preparado para o Workshop Claude Sem Frescura — Módulo Claude Code*
