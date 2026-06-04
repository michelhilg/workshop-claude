---
name: gerar-outputs
description: Usa o NotebookLM para gerar quatro formatos de output a partir de um notebook já alimentado com as fontes da wiki/: infográfico (png), quiz (json), mapa mental (json) e podcast (mp3). Salva tudo em outputs/. Pré-requisito: notebook criado e com fontes adicionadas.
---

# Skill: gerar-outputs

## O que esta skill faz

Usa o NotebookLM (via skill `notebooklm`) para gerar quatro formatos de output a partir de um notebook já criado e alimentado com as fontes da `wiki/`. Os artefatos gerados são salvos na pasta `outputs/`.

**Pré-requisito obrigatório:** o notebook deve existir no NotebookLM e ter pelo menos um arquivo da `wiki/` adicionado como fonte. Se isso não foi feito, execute a skill `notebooklm` primeiro.

---

## Outputs gerados

| Formato | Arquivo salvo | O que é |
|---|---|---|
| Infográfico | `outputs/infografico.png` | Resumo visual do conteúdo do notebook |
| Quiz | `outputs/quiz.json` | Perguntas e respostas geradas a partir das fontes |
| Mapa mental | `outputs/mindmap.json` | Estrutura hierárquica dos temas do notebook |
| Podcast | `outputs/podcast.mp3` | Audio Overview — dois apresentadores discutindo o conteúdo |

---

## Passo a passo de execução

### Passo 1 — Verificar o notebook e configurar o idioma

Antes de gerar qualquer output:
1. Use a skill `notebooklm` para confirmar que o notebook existe
2. Confirme que há pelo menos uma fonte adicionada
3. Se o notebook não existir ou não tiver fontes, informe o usuário e pare
4. **Defina o idioma para português brasileiro:**
   ```bash
   notebooklm language set pt_BR
   ```
   Confirme que o comando retornou sucesso antes de continuar. Se `pt_BR` não estiver disponível, tente `pt`. Se nenhum funcionar, registre em `outputs/pendencias.txt` e informe o usuário — o conteúdo pode sair em inglês.

### Passo 2 — Gerar os outputs em sequência

Gere um output por vez, na seguinte ordem. Após cada geração, salve o arquivo em `outputs/` antes de continuar.

**1. Infográfico**
- Use o recurso de geração de infográfico do NotebookLM
- Aguarde a geração completar
- Baixe e salve como `outputs/infografico.png`
- Confirme que o arquivo foi salvo antes de continuar

**2. Quiz**
- Use o recurso de geração de quiz/estudo do NotebookLM
- Aguarde a geração completar
- Salve o conteúdo como `outputs/quiz.json` ou `outputs/quiz.txt` conforme o formato retornado
- O quiz deve conter perguntas, alternativas e respostas corretas

**3. Mapa mental**
- Use o recurso de mapa mental do NotebookLM
- Aguarde a geração completar
- Baixe com: `notebooklm download mind-map outputs/mindmap.json`
- **O arquivo gerado deve seguir obrigatoriamente o formato padrão abaixo.** Verifique após o download. Se o formato estiver diferente, converta antes de salvar:

```json
{
  "name": "Nome do nó raiz",
  "children": [
    {
      "name": "Nó de nível 1",
      "children": [
        {
          "name": "Nó de nível 2"
        }
      ]
    }
  ]
}
```

Regras do formato:
- Cada nó tem obrigatoriamente `"name"` (string)
- `"children"` é opcional — omita em nós folha (não use `"children": []`)
- A estrutura é recursiva — qualquer profundidade é válida
- Este formato é lido pelo visualizador `recursos/mindmap.html` via D3.js. Qualquer desvio quebrará a renderização.

**4. Podcast (Audio Overview)**
- Use o recurso Audio Overview do NotebookLM
- Este é o formato que demora mais — aguarde sem interromper
- Salve o arquivo de áudio como `outputs/podcast.mp3`
- Se o download não estiver disponível imediatamente, registre em `outputs/pendencias.txt` e informe o usuário

### Passo 3 — Confirmar e reportar

Após tentar gerar todos os outputs, liste:
- Quais foram gerados com sucesso e onde estão salvos
- Quais falharam ou estão pendentes e por quê
- Tamanho aproximado dos arquivos gerados

---

## Tratamento de falhas

**Se um recurso não estiver disponível no NotebookLM:**
- Registre em `outputs/pendencias.txt`: nome do formato, motivo do erro, data
- Continue tentando gerar os demais — não pare o fluxo inteiro por uma falha

**Se a conexão com o NotebookLM cair:**
- Informe o usuário imediatamente
- Não tente reconectar em loop
- Relate o que já foi gerado e o que está pendente

**Se o arquivo não puder ser salvo em `outputs/`:**
- Tente salvar com nome alternativo (ex.: `infografico_v2.png`)
- Se persistir, informe o usuário com o erro completo

---

## Comportamento esperado ao acionar

Quando o usuário disser algo como:
- "Gere todos os outputs do notebook X"
- "Quero o podcast e o quiz do notebook Y"
- "Gera os materiais de treinamento"

Execute o passo a passo acima. Se o usuário pedir apenas um formato específico, gere somente aquele e salve normalmente em `outputs/`.

---

## O que NÃO fazer

- Não gere outputs antes de confirmar que o notebook tem fontes
- Não invente conteúdo de quiz ou mapa mental — tudo deve vir do NotebookLM
- Não sobrescreva arquivos existentes em `outputs/` sem avisar o usuário
- Não considere o fluxo concluído enquanto houver outputs pendentes sem registro
