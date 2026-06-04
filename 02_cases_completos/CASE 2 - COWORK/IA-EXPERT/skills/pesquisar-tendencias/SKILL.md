# Skill: pesquisar-tendencias

**Gatilho:** quando o usuário disser "pesquisar tendências" (ou variações: "pesquisa tendências", "atualizar tendências", "rodar pesquisa").

## O que fazer

1. **LER** `tendencias/inputs/temas.md` — minha lista de temas. NUNCA escrever neste arquivo.
2. **LER** `memory/tendencias/criterios.md`, `memory/tendencias/fontes.md` e `memory/tendencias/glossario-ia.md` para calibrar a busca.
3. Para **CADA tema** da lista, fazer web search nativo focado nos últimos 7 dias no nicho de Inteligência Artificial. Priorizar lançamentos, mudanças de preço, features novas e debates em alta. Ignorar rumor não confirmado.
4. **Classificar** cada achado:
   - `categoria` — qual dos 10 temas da lista
   - `resumo` — 1–2 frases do que aconteceu
   - `por_que_importa` — 1 frase para o público de creators/empreendedores de IA brasileiros ("o que isso muda pra mim")
   - `calor` — `alto` / `médio` / `baixo` conforme `criterios.md`
   - `fonte_titulo`, `fonte_url`, `publicado_em`
5. **Dedupe** por `fonte_url` dentro deste run.
6. **ESCREVER** `tendencias/data/tendencias-AAAA-MM-DD.json` (data de hoje, fuso America/Sao_Paulo). Sobrescrever se já existir arquivo do dia.
7. **ESCREVER** `tendencias/data/ultima-pesquisa.json` — cópia idêntica do snapshot de hoje.
8. **GERAR** `tendencias/outputs/dashboard-tendencias.html` — seguir exatamente as instruções desta seção.
9. Listar em `temas_sem_movimento` os temas que **não** tiveram achado neste run.

---

## ⚠️ Regras críticas

- Escreve SOMENTE em `tendencias/data/` e `tendencias/outputs/`. NUNCA em `tendencias/inputs/`.
- O HTML gerado deve ser **idêntico em estrutura** a cada run. Dados mudam; layout não.
- O design system de referência está em `design-system-dashboard-noticias.json` (mesma pasta desta skill).

---

## Esquema do JSON de saída (steps 6 e 7)

```json
{
  "data": "AAAA-MM-DD",
  "nicho": "Inteligência Artificial",
  "gerado_em": "AAAA-MM-DDTHH:MM:SS-03:00",
  "itens": [
    {
      "titulo": "...",
      "categoria": "...",
      "resumo": "...",
      "por_que_importa": "...",
      "calor": "alto|médio|baixo",
      "fonte_titulo": "...",
      "fonte_url": "https://...",
      "publicado_em": "AAAA-MM-DD"
    }
  ],
  "temas_sem_movimento": ["tema A", "tema B"]
}
```

---

## Step 8 — Geração do HTML (instrução detalhada)

### Regra fundamental — NUNCA escreva o HTML manualmente

**O template abaixo é imutável.** Claude não escreve, reescreve nem reconstrói o HTML de memória — nunca. A única operação permitida é **substituição mecânica** do `{{JSON_DATA_INLINE}}` pelo JSON dos dados. Todo o resto do arquivo deve ser copiado byte a byte.

**Método obrigatório — usar script Python:**

```python
import json, re

with open('tendencias/data/ultima-pesquisa.json', 'r') as f:
    data = json.load(f)

with open('skills/pesquisar-tendencias/SKILL.md', 'r') as f:
    skill = f.read()

match = re.search(r'```html\n(.*?)```', skill, re.DOTALL)
html = match.group(1).replace('{{JSON_DATA_INLINE}}', json.dumps(data, ensure_ascii=False))

with open('tendencias/outputs/dashboard-tendencias.html', 'w') as f:
    f.write(html)
```

Adaptar os paths conforme o ambiente (bash usa `/sessions/.../mnt/IA-EXPERT/` como prefixo). Executar via `mcp__workspace__bash`. Não usar Write ou Edit diretamente no HTML final.

**Se Claude se pegar "escrevendo HTML" — parar imediatamente.** Isso é sinal de que está ignorando esta instrução.

### Preparação dos dados antes de gerar

1. **Ordenar** `itens` por calor: `alto` primeiro, depois `médio`, depois `baixo`. Dentro do mesmo calor, manter ordem da pesquisa.
2. **Mapear** o campo `calor` para label e classe CSS:
   - `"alto"`  → label `"QUENTE"`, classe `"heat-alto"`
   - `"médio"` → label `"MORNO"`,  classe `"heat-medio"` *(sem acento — evita problema de encoding)*
   - `"baixo"` → label `"FRIO"`,   classe `"heat-baixo"`
3. **Formatar datas:**
   - `publicado_em` (`AAAA-MM-DD`) → `"DD Mmm AAAA"` (ex.: `"03 Jun 2026"`). Meses: `Jan Fev Mar Abr Mai Jun Jul Ago Set Out Nov Dez`.
   - `gerado_em` (ISO-8601 com offset) → `"DD Mmm AAAA · HHhMM"` (ex.: `"03 Jun 2026 · 14h30"`).
4. **Serializar** o JSON completo como `JSON.stringify(data)` para embutir no `<script>`. Não formatar com quebras de linha.

### Template HTML — copiar verbatim, substituir apenas `{{...}}`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Painel de Tendências · IA Sem Frescura</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    /* === TOKENS === */
    :root {
      --green-deep: #0E3A2F;
      --cream:      #F5EFE3;
      --cream-dark: #EDE7D6;
      --coral:      #E8865A;
      --mint:       #A8E6C9;
      --mint-muted: #8FB89E;
      --pill-light: #E7DFCF;
      --hairline:   #C9BFA9;
      --text-muted: #5B6B61;

      --f-display: 'Hanken Grotesk', system-ui, sans-serif;
      --f-mono:    'JetBrains Mono', ui-monospace, monospace;

      --t-page-title:    1.75rem;
      --t-section-title: 0.6875rem;
      --t-card-title:    1rem;
      --t-body:          0.875rem;
      --t-importa:       0.875rem;
      --t-meta:          0.6875rem;
      --t-badge:         0.625rem;
      --t-filter:        0.6875rem;
      --t-timestamp:     0.75rem;

      --card-pad:    20px;
      --grid-gap:    16px;
      --r-badge:     999px;
      --r-card:      16px;
      --r-pill:      999px;
      --shadow-card: 0 2px 8px rgba(14,58,47,0.07), 0 0 0 1px #C9BFA9;
    }

    /* === RESET === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--f-display);
      background: var(--cream-dark);
      color: var(--green-deep);
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
    }

    /* === PAGE WRAPPER === */
    .page-wrap { max-width: 1200px; margin: 0 auto; padding-bottom: 56px; }

    /* === HEADER === */
    .page-header {
      background: var(--green-deep);
      padding: 28px 40px;
      display: flex;
      align-items: center;
      gap: 24px;
    }
    .brand-badge {
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--mint);
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      border: 1px solid rgba(168,230,201,0.3);
      padding: 5px 12px;
      border-radius: var(--r-pill);
      flex-shrink: 0;
    }
    .asterisk { color: var(--coral); }
    .header-right { flex: 1; min-width: 0; }
    .page-title {
      font-size: var(--t-page-title);
      font-weight: 800;
      color: var(--cream);
      line-height: 1.1;
    }
    .timestamp {
      font-family: var(--f-mono);
      font-size: var(--t-timestamp);
      color: var(--mint-muted);
      margin-top: 4px;
    }

    /* === FILTER BAR === */
    .filter-bar {
      background: var(--cream-dark);
      padding: 14px 40px;
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      border-bottom: 1px solid var(--hairline);
      position: sticky;
      top: 0;
      z-index: 10;
    }
    .filter-group { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
    .filter-group-label {
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-right: 4px;
    }
    .filter-divider { width: 1px; height: 20px; background: var(--hairline); }
    .filter-pill {
      font-family: var(--f-mono);
      font-size: var(--t-filter);
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 5px 12px;
      border-radius: var(--r-pill);
      border: 1px solid var(--hairline);
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      transition: background 0.15s, color 0.15s, border-color 0.15s;
    }
    .filter-pill:hover,
    .filter-pill.active                  { background: var(--green-deep); color: var(--cream); border-color: var(--green-deep); }
    .filter-pill[data-heat="alto"].active  { background: var(--coral);     border-color: var(--coral);     color: #fff; }
    .filter-pill[data-heat="médio"].active { background: var(--mint);      border-color: var(--mint);      color: var(--green-deep); }
    .filter-pill[data-heat="baixo"].active { background: var(--pill-light); border-color: var(--hairline); color: var(--text-muted); }

    /* === CONTENT AREA === */
    .content-area { padding: 32px 40px 0; }

    /* === SECTION HEADER === */
    .section-header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 20px; }
    .section-title {
      font-family: var(--f-mono);
      font-size: var(--t-section-title);
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
    }
    .section-count {
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      color: var(--mint-muted);
    }

    /* === NEWS GRID === */
    .news-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: var(--grid-gap);
      align-items: start;
    }
    @media (max-width: 899px) { .news-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 599px) { .news-grid { grid-template-columns: 1fr; } }

    /* === NEWS CARD === */
    .news-card {
      background: var(--cream);
      border-radius: var(--r-card);
      box-shadow: var(--shadow-card);
      padding: var(--card-pad);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .card-top    { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .heat-badge  {
      font-family: var(--f-mono);
      font-size: var(--t-badge);
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: var(--r-badge);
      flex-shrink: 0;
    }
    .heat-badge.heat-alto  { background: var(--coral);     color: #fff; }
    .heat-badge.heat-medio { background: #e8c84a;          color: #5a4200; }
    .heat-badge.heat-baixo { background: var(--pill-light); color: var(--text-muted); }
    .news-card.heat-alto   { border-left: 3px solid var(--coral); }
    .news-card.heat-medio  { border-left: 3px solid #e8c84a; background: #fefbe8; }
    .news-card.heat-baixo  { border-left: 3px solid var(--hairline); }
    .card-category {
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--mint-muted);
    }
    .card-title   { font-size: var(--t-card-title); font-weight: 700; line-height: 1.35; }
    .card-summary { font-size: var(--t-body); line-height: 1.55; }
    .card-importa {
      background: rgba(14,58,47,0.04);
      border-left: 2px solid var(--mint);
      padding: 10px 12px;
      border-radius: 0 8px 8px 0;
    }
    .importa-label {
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--mint-muted);
      display: block;
      margin-bottom: 4px;
    }
    .importa-text { font-size: var(--t-importa); font-weight: 500; line-height: 1.5; }
    .card-footer  {
      margin-top: auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 8px;
      border-top: 1px solid var(--hairline);
    }
    .card-source {
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      color: var(--coral);
      text-decoration: none;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 70%;
    }
    .card-source:hover { text-decoration: underline; }
    .card-date {
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      color: var(--text-muted);
      white-space: nowrap;
      flex-shrink: 0;
    }

    /* === EMPTY STATE === */
    .empty-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 48px 24px;
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
    }

    /* === NO MOVEMENT === */
    .no-movement-section { padding: 32px 0 0; }
    .no-movement-pills   { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
    .topic-pill {
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      letter-spacing: 0.06em;
      padding: 4px 12px;
      border-radius: var(--r-pill);
      background: var(--pill-light);
      color: var(--text-muted);
      border: 1px solid var(--hairline);
    }

    /* === PAGE FOOTER === */
    .page-footer {
      padding: 24px 0 8px;
      text-align: center;
      font-family: var(--f-mono);
      font-size: var(--t-meta);
      color: var(--text-muted);
      border-top: 1px solid var(--hairline);
      margin-top: 32px;
      letter-spacing: 0.06em;
    }

    /* === MOBILE === */
    @media (max-width: 599px) {
      .page-header  { padding: 20px 16px; flex-direction: column; align-items: flex-start; gap: 12px; }
      .filter-bar   { padding: 12px 16px; }
      .content-area { padding: 20px 16px 0; }
    }
  </style>
</head>
<body>
<div class="page-wrap">

  <!-- HEADER -->
  <header class="page-header">
    <div class="brand-badge"><span class="asterisk">✳</span> IA Sem Frescura</div>
    <div class="header-right">
      <h1 class="page-title">Painel de Tendências</h1>
      <p class="timestamp" id="ts"></p>
    </div>
  </header>

  <!-- FILTER BAR -->
  <div class="filter-bar">
    <div class="filter-group" id="cat-filters">
      <span class="filter-group-label">Tema</span>
    </div>
    <div class="filter-divider"></div>
    <div class="filter-group" id="heat-filters">
      <span class="filter-group-label">Calor</span>
      <button class="filter-pill active" data-heat="all">Todos</button>
      <button class="filter-pill" data-heat="alto">QUENTE</button>
      <button class="filter-pill" data-heat="médio">MORNO</button>
      <button class="filter-pill" data-heat="baixo">FRIO</button>
    </div>
  </div>

  <!-- CONTENT -->
  <div class="content-area">
    <div class="section-header">
      <span class="section-title">Tendências de IA</span>
      <span class="section-count" id="count"></span>
    </div>
    <div class="news-grid" id="grid"></div>

    <div class="no-movement-section" id="no-movement" style="display:none">
      <span class="section-title">Temas sem movimento</span>
      <div class="no-movement-pills" id="no-movement-pills"></div>
    </div>

    <footer class="page-footer" id="foot"></footer>
  </div>

</div>
<script>
const DATA = {{JSON_DATA_INLINE}};

const MONTHS = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];

function fmtDate(iso) {
  if (!iso) return '';
  const [y, m, d] = iso.split('T')[0].split('-');
  return `${d} ${MONTHS[+m - 1]} ${y}`;
}

function fmtTimestamp(iso) {
  if (!iso) return '';
  const clean = iso.replace(/[+-]\d{2}:\d{2}$/, '').replace('Z', '');
  const [datePart, timePart = '00:00'] = clean.split('T');
  const [y, m, d] = datePart.split('-');
  const [h, min] = timePart.split(':');
  return `${d} ${MONTHS[+m - 1]} ${y} · ${h}h${min}`;
}

const HEAT = {
  'alto':  { label: 'QUENTE', cls: 'heat-alto'  },
  'médio': { label: 'MORNO',  cls: 'heat-medio' },
  'baixo': { label: 'FRIO',   cls: 'heat-baixo' }
};

const ORDER = { alto: 0, 'médio': 1, baixo: 2 };
const sorted = [...DATA.itens].sort((a, b) => (ORDER[a.calor] ?? 9) - (ORDER[b.calor] ?? 9));

let activeCat  = 'all';
let activeHeat = 'all';

function renderGrid(items) {
  const grid = document.getElementById('grid');
  const count = document.getElementById('count');
  grid.innerHTML = '';
  if (!items.length) {
    grid.innerHTML = '<p class="empty-state">Nenhum resultado para este filtro.</p>';
    count.textContent = '';
    return;
  }
  count.textContent = `${items.length} item${items.length !== 1 ? 's' : ''}`;
  items.forEach(item => {
    const h = HEAT[item.calor] || { label: item.calor, cls: 'heat-baixo' };
    const el = document.createElement('article');
    el.className = 'news-card ' + h.cls;
    el.dataset.heat = item.calor;
    el.dataset.cat  = item.categoria;
    el.innerHTML = `
      <div class="card-top">
        <span class="heat-badge ${h.cls}">${h.label}</span>
        <span class="card-category">${item.categoria}</span>
      </div>
      <h2 class="card-title">${item.titulo}</h2>
      <p class="card-summary">${item.resumo}</p>
      <div class="card-importa">
        <span class="importa-label">Por que importa</span>
        <p class="importa-text">${item.por_que_importa}</p>
      </div>
      <footer class="card-footer">
        <a class="card-source" href="${item.fonte_url}" target="_blank" rel="noopener">${item.fonte_titulo}</a>
        <time class="card-date">${fmtDate(item.publicado_em)}</time>
      </footer>`;
    grid.appendChild(el);
  });
}

function applyFilters() {
  const visible = sorted.filter(i => {
    const hOk = activeHeat === 'all' || i.calor === activeHeat;
    const cOk  = activeCat  === 'all' || i.categoria === activeCat;
    return hOk && cOk;
  });
  renderGrid(visible);
}

function setActive(group, btn) {
  group.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

document.getElementById('heat-filters').querySelectorAll('[data-heat]').forEach(btn => {
  btn.addEventListener('click', () => {
    activeHeat = btn.dataset.heat;
    setActive(document.getElementById('heat-filters'), btn);
    applyFilters();
  });
});

(function buildCatFilters() {
  const cats = ['all', ...new Set(sorted.map(i => i.categoria))];
  const group = document.getElementById('cat-filters');
  cats.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'filter-pill' + (cat === 'all' ? ' active' : '');
    btn.dataset.cat = cat;
    btn.textContent = cat === 'all' ? 'Todos' : cat;
    btn.addEventListener('click', () => {
      activeCat = cat;
      setActive(group, btn);
      applyFilters();
    });
    group.appendChild(btn);
  });
})();

(function renderNoMovement() {
  const temas = DATA.temas_sem_movimento || [];
  if (!temas.length) return;
  document.getElementById('no-movement').style.display = 'block';
  const pills = document.getElementById('no-movement-pills');
  temas.forEach(t => {
    const span = document.createElement('span');
    span.className = 'topic-pill';
    span.textContent = t;
    pills.appendChild(span);
  });
})();

document.getElementById('ts').textContent   = 'Última atualização: ' + fmtTimestamp(DATA.gerado_em);
document.getElementById('foot').textContent = `IA Sem Frescura · Gerado por Claude · ${DATA.data}`;
applyFilters();
</script>
</body>
</html>
```

### Onde substituir `{{JSON_DATA_INLINE}}`

Substituir a marcação `{{JSON_DATA_INLINE}}` pelo resultado de `JSON.stringify(data)` — o objeto JSON completo do step 6, serializado em uma única linha sem formatação adicional.

**Exemplo:**
```html
const DATA = {"data":"2026-06-03","nicho":"Inteligência Artificial","gerado_em":"2026-06-03T14:30:00-03:00","itens":[...],"temas_sem_movimento":[]};
```

### Checklist antes de salvar o HTML

- [ ] HTML gerado via script Python — **não** escrito manualmente
- [ ] `{{JSON_DATA_INLINE}}` foi substituído pelo JSON real (nenhum `{{` restante no arquivo)
- [ ] Verificar com `grep -c 'news-card'` no output: deve bater com `len(data['itens'])`
- [ ] CSS não foi alterado em relação ao template (confirmar com diff mental ou grep)
- [ ] Nenhuma cor, tamanho ou classe inventada fora do template
- [ ] Cards ordenados: alto → médio → baixo
- [ ] Seção "Temas sem movimento" oculta se a lista estiver vazia
- [ ] Fontes carregando do Google Fonts CDN
