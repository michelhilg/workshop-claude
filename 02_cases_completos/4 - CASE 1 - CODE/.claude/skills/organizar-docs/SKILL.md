---
name: organizar-docs
description: Lê todos os arquivos em inputs/ (txt, pptx, xlsx, pdf), extrai o conhecimento útil e gera múltiplos arquivos .txt temáticos em wiki/. Acionar quando inputs/ foi atualizado ou quando wiki/ ainda não existe.
---

# Skill: organizar-docs

## O que esta skill faz

Lê todos os arquivos da pasta `inputs/` — independentemente do formato — extrai o conhecimento útil e gera múltiplos arquivos `.txt` temáticos na pasta `wiki/`. O objetivo é transformar material bruto e desorganizado em documentação limpa, estruturada e pronta para ser subida no NotebookLM.

---

## Quando usar

Acione esta skill quando:
- A pasta `wiki/` está vazia ou desatualizada
- Novos arquivos foram adicionados em `inputs/`
- O usuário pedir para "organizar os documentos" ou "gerar a wiki"

---

## Passo a passo de execução

### Passo 1 — Inventariar os inputs

Liste todos os arquivos em `inputs/` antes de começar. Para cada arquivo:
- `.txt` → leia diretamente
- `.pptx` → extraia o texto de cada slide
- `.xlsx` → leia cada aba como texto estruturado
- `.pdf` → extraia o texto corrido

Se um arquivo não puder ser lido, registre em `outputs/pendencias.txt` e continue.

### Passo 2 — Extrair e consolidar o conhecimento

Leia todos os arquivos de uma vez. Ao consolidar:
- **Ignore** metadados irrelevantes (datas de edição, cabeçalhos de sistema, trechos inaudíveis marcados)
- **Preserve** regras, decisões, processos, métricas, pendências e aprendizados
- **Resolva contradições** usando o dado mais recente ou mais detalhado; anote a contradição se for relevante
- **Mantenha pendências** como pendências — não invente resoluções para itens em aberto

### Passo 3 — Gerar os arquivos temáticos

Crie um arquivo `.txt` por tema em `wiki/`. Cada arquivo deve:
- Ter um nome descritivo em kebab-case (ex.: `processo-gravacao.txt`)
- Começar com um título e uma frase de objetivo
- Ser escrito em português claro e direto
- Ter no mínimo 150 e no máximo 400 linhas — se um tema for muito grande, divida em dois arquivos

**Temas esperados a partir dos inputs disponíveis:**

| Arquivo wiki | Conteúdo esperado |
|---|---|
| `processo-gravacao.txt` | Equipamento, configurações, boas práticas de gravação, o que fazer e evitar |
| `fluxo-aprovacao.txt` | Briefing, edição, revisão, aprovação, comunicação com editoras (Carol e Jana) |
| `calendario-editorial.txt` | Frequência, formatos, cadência semanal, regras de agendamento, horários |
| `metricas-e-kpis.txt` | Métricas que importam, metas, critérios de sucesso por formato, o que ignorar |
| `gestao-equipe.txt` | Papéis (Carol, Jana, Rodrigo), como se comunicar, SLAs, regras de delegação |
| `estrategia-conteudo.txt` | POV, tipos de conteúdo que performam, formatos, regras de backlog, o que não funciona |

> Esses são os temas esperados. Se durante a leitura dos inputs surgir um tema relevante não listado acima, crie o arquivo correspondente. Se um tema esperado não tiver dados suficientes, omita o arquivo e registre a ausência em `outputs/pendencias.txt`.

### Passo 4 — Confirmar e reportar

Após gerar todos os arquivos, liste:
- Quantos arquivos foram gerados em `wiki/`
- Nome e descrição de cada um
- Eventuais pendências registradas

---

## Formato de cada arquivo wiki

```
# [Título do tema]

**Objetivo:** [Uma frase descrevendo o que este documento cobre]
**Última atualização:** [data de hoje]
**Fonte:** Consolidado a partir dos arquivos em inputs/

---

## [Seção 1]

[Conteúdo limpo e estruturado]

## [Seção 2]

[Conteúdo limpo e estruturado]

---

## Pendências e itens em aberto

[Lista de itens que estavam incompletos nos inputs originais — não invente resolução]
```

---

## O que NÃO fazer

- Não invente informações que não estão nos inputs
- Não delete ou modifique nenhum arquivo em `inputs/`
- Não gere um único arquivo gigante com tudo misturado
- Não use markdown complexo — o objetivo é `.txt` limpo compatível com NotebookLM
- Não omita pendências — se estava em aberto no input, fica em aberto na wiki
