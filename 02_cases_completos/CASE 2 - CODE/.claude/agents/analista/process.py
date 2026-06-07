# -*- coding: utf-8 -*-
"""
AdGrowth CRM Pipeline - Etapa 2: Análise e Enriquecimento
Analista Agent - process.py
"""

import json
import os
import sys
from datetime import datetime, timezone
from collections import defaultdict, Counter

# ─────────────────────────── Paths ───────────────────────────
BASE = r"C:\Users\Lucas Xiang\Desktop\AdGrowth"
INPUT_DIR = os.path.join(BASE, ".claude", "data", "dadosBrutos")
OUTPUT_DIR = os.path.join(BASE, ".claude", "data", "processados")
CONFIG_PATH = os.path.join(BASE, ".claude", "agents", "analista", "config.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

ENRICHED_AT = datetime.now(timezone.utc).isoformat()

# ─────────────────────────── Load config ─────────────────────
print("Loading config...")
with open(CONFIG_PATH, encoding="utf-8") as f:
    config = json.load(f)

CANAL_MAP = config["CANAL_MAP"]
ETAPA_MAP = config["ETAPA_MAP"]

# ─────────────────────────── Load input files ────────────────
def load_json(filename):
    path = os.path.join(INPUT_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"FATAL: arquivo de entrada ausente: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

print("Loading input files...")
leads_raw       = load_json("leads_raw.json")
campaigns_raw   = load_json("campaigns.json")
interactions_raw = load_json("interactions.json")
pipeline_raw    = load_json("pipeline_config.json")

print(f"  leads_raw:       {len(leads_raw):,}")
print(f"  campaigns:       {len(campaigns_raw):,}")
print(f"  interactions:    {len(interactions_raw):,}")
print(f"  pipeline_config: {len(pipeline_raw):,}")

# ─────────────────────────── Build indexes ───────────────────
print("Building indexes...")

# 1. campaigns_index
campaigns_index = {}
for c in campaigns_raw:
    cid = c.get("campanha_id")
    if cid:
        campaigns_index[cid] = {
            "nome_campanha":   c.get("nome_campanha"),
            "canal_campanha":  c.get("canal"),
            "objetivo":        c.get("objetivo"),
            "data_inicio":     c.get("data_inicio"),
            "data_fim":        c.get("data_fim"),
            "investimento":    c.get("investimento"),
            "utm_source":      c.get("utm_source"),
            "utm_medium":      c.get("utm_medium"),
            "utm_campaign":    c.get("utm_campaign"),
            "persona_alvo":    c.get("persona_alvo"),
            "oferta":          c.get("oferta"),
        }
print(f"  campaigns_index: {len(campaigns_index)} entries")

# 2. interactions_index  (lead_id → aggregated)
interactions_by_lead = defaultdict(list)
for inter in interactions_raw:
    lid = inter.get("lead_id")
    if lid:
        interactions_by_lead[lid].append(inter)

def mode_or_none(lst):
    if not lst:
        return None
    c = Counter(lst)
    return c.most_common(1)[0][0]

interactions_index = {}
for lid, inters in interactions_by_lead.items():
    dates = [i.get("data_interacao") for i in inters if i.get("data_interacao")]
    dates_sorted = sorted(dates)
    sentimentos = [i.get("sentimento") for i in inters if i.get("sentimento")]
    objecoes = [i.get("objecao_principal") for i in inters if i.get("objecao_principal")]
    interactions_index[lid] = {
        "total_interacoes":      len(inters),
        "ultima_interacao":      dates_sorted[-1] if dates_sorted else None,
        "sentimento_dominante":  mode_or_none(sentimentos),
        "principal_objecao":     mode_or_none(objecoes),
    }
print(f"  interactions_index: {len(interactions_index)} leads com interações")

# 3. pipeline_index  (etapa_funil → metadata)
pipeline_index = {}
for p in pipeline_raw:
    etapa = p.get("etapa_funil")
    if etapa:
        prob_str = p.get("probabilidade_fechamento", "0%").replace("%", "")
        try:
            prob = float(prob_str)
        except ValueError:
            prob = 0.0
        pipeline_index[etapa] = {
            "ordem":                   int(p.get("ordem", 0)),
            "categoria":               p.get("categoria"),
            "probabilidade_fechamento": prob,
        }
print(f"  pipeline_index: {len(pipeline_index)} etapas")

# ─────────────────────────── Normalize & Enrich leads ────────
print("Processing leads...")

leads_clean = []
patterns = []  # inconsistências

stats = {
    "total": 0,
    "canal_normalizado": 0,
    "canal_nao_mapeado": 0,
    "etapa_normalizada": 0,
    "etapa_nao_mapeada": 0,
    "sem_responsavel": 0,
    "sem_campanha": 0,
    "com_interacoes": 0,
    "sem_interacoes": 0,
    "com_inconsistencias": 0,
}

for lead in leads_raw:
    stats["total"] += 1
    lead_id = lead.get("lead_id", f"UNKNOWN-{stats['total']}")
    inconsistencias = []

    # ── Canal normalization ──
    canal_original = lead.get("canal")
    if canal_original and canal_original in CANAL_MAP:
        canal_norm = CANAL_MAP[canal_original]
        canal_normalizado = True
        stats["canal_normalizado"] += 1
    else:
        canal_norm = canal_original  # keep original
        canal_normalizado = False
        stats["canal_nao_mapeado"] += 1
        if canal_original:
            inconsistencias.append({
                "tipo": "canal_nao_mapeado",
                "campo": "canal",
                "valor_original": canal_original
            })

    # ── Etapa normalization ──
    etapa_original = lead.get("etapa_funil")
    if etapa_original and etapa_original in ETAPA_MAP:
        etapa_norm = ETAPA_MAP[etapa_original]
        etapa_normalizada = True
        stats["etapa_normalizada"] += 1
    else:
        etapa_norm = etapa_original  # keep original
        etapa_normalizada = False
        stats["etapa_nao_mapeada"] += 1
        if etapa_original:
            inconsistencias.append({
                "tipo": "etapa_nao_mapeada",
                "campo": "etapa_funil",
                "valor_original": etapa_original
            })

    # ── Responsável ──
    responsavel = lead.get("responsavel") or lead.get("responsavel_id")
    if not responsavel:
        stats["sem_responsavel"] += 1
        inconsistencias.append({"tipo": "sem_responsavel", "campo": "responsavel", "valor_original": None})

    # ── Campanha ──
    campanha_id = lead.get("campanha_id")
    campanha_info = None
    if campanha_id and campanha_id in campaigns_index:
        campanha_info = campaigns_index[campanha_id]
    else:
        stats["sem_campanha"] += 1
        if campanha_id:
            inconsistencias.append({"tipo": "campanha_nao_encontrada", "campo": "campanha_id", "valor_original": campanha_id})
        else:
            inconsistencias.append({"tipo": "sem_campanha_id", "campo": "campanha_id", "valor_original": None})

    # ── Pipeline enrichment ──
    pipeline_info = None
    if etapa_norm and etapa_norm in pipeline_index:
        pipeline_info = pipeline_index[etapa_norm]
    else:
        # try mapped canonical names in pipeline_index
        for pk in pipeline_index:
            if etapa_norm and pk.lower() == etapa_norm.lower():
                pipeline_info = pipeline_index[pk]
                break

    # ── Interactions enrichment ──
    inter_info = interactions_index.get(lead_id)
    if inter_info:
        stats["com_interacoes"] += 1
    else:
        stats["sem_interacoes"] += 1
        inter_info = {
            "total_interacoes": 0,
            "ultima_interacao": None,
            "sentimento_dominante": None,
            "principal_objecao": None,
        }

    # ── Score parse ──
    score_raw = lead.get("score_crm")
    try:
        score = int(score_raw) if score_raw is not None else None
    except (ValueError, TypeError):
        score = None

    # ── Valor estimado ──
    valor_raw = lead.get("valor_estimado")
    try:
        valor = float(valor_raw) if valor_raw is not None else None
    except (ValueError, TypeError):
        valor = None

    # ── Build enriched lead ──
    enriched = {
        # original fields preserved
        "lead_id":              lead_id,
        "nome":                 lead.get("nome"),
        "email":                lead.get("email"),
        "telefone":             lead.get("telefone"),
        "empresa":              lead.get("empresa"),
        "cargo":                lead.get("cargo"),
        "segmento":             lead.get("segmento"),
        "tamanho_empresa":      lead.get("tamanho_empresa"),
        "cidade":               lead.get("cidade"),
        "estado":               lead.get("estado"),
        "origem":               lead.get("origem"),
        # normalized
        "canal":                canal_norm,
        "canal_original":       canal_original,
        "etapa_funil":          etapa_norm,
        "etapa_funil_original": etapa_original,
        "score_crm":            score,
        "valor_estimado":       valor,
        "status":               lead.get("status"),
        "responsavel_id":       lead.get("responsavel_id"),
        "responsavel":          lead.get("responsavel"),
        "campanha_id":          campanha_id,
        "data_entrada":         lead.get("data_entrada"),
        "observacoes_vendedor": lead.get("observacoes_vendedor"),
        "proxima_acao":         lead.get("proxima_acao"),
        # enrichment flags
        "_canal_normalizado":   canal_normalizado,
        "_etapa_normalizada":   etapa_normalizada,
        # enrichment data
        "campanha":             campanha_info,
        "pipeline":             pipeline_info,
        "interacoes":           inter_info,
        "_enriched_at":         ENRICHED_AT,
    }

    leads_clean.append(enriched)

    if inconsistencias:
        stats["com_inconsistencias"] += 1
        for inc in inconsistencias:
            patterns.append({
                "lead_id":  lead_id,
                "tipo":     inc["tipo"],
                "campo":    inc["campo"],
                "valor_original": inc["valor_original"],
            })

print(f"  Processed {stats['total']:,} leads")
print(f"  Canal normalizado:    {stats['canal_normalizado']:,} | Não mapeado: {stats['canal_nao_mapeado']:,}")
print(f"  Etapa normalizada:    {stats['etapa_normalizada']:,} | Não mapeada: {stats['etapa_nao_mapeada']:,}")
print(f"  Sem responsável:      {stats['sem_responsavel']:,}")
print(f"  Sem campanha:         {stats['sem_campanha']:,}")
print(f"  Com interações:       {stats['com_interacoes']:,}")
print(f"  Com inconsistências:  {stats['com_inconsistencias']:,}")

# ─────────────────────────── Aggregate metrics ───────────────
print("Calculating aggregate metrics...")

# Helper: parse data_entrada
def parse_date(ds):
    if not ds:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(ds).strip(), fmt)
        except ValueError:
            continue
    return None

# ── 1. Funnel summary per etapa ──
funnel_data = defaultdict(lambda: {"count": 0, "valor_total": 0.0, "scores": []})
for lead in leads_clean:
    etapa = lead.get("etapa_funil") or "Desconhecida"
    funnel_data[etapa]["count"] += 1
    v = lead.get("valor_estimado")
    if v:
        funnel_data[etapa]["valor_total"] += v
    s = lead.get("score_crm")
    if s is not None:
        funnel_data[etapa]["scores"].append(s)

total_leads = stats["total"]
funnel_summary = {}
for etapa, d in funnel_data.items():
    scores = d["scores"]
    pipeline_meta = pipeline_index.get(etapa, {})
    funnel_summary[etapa] = {
        "contagem":           d["count"],
        "percentual_total":   round(d["count"] / total_leads * 100, 2),
        "valor_total":        round(d["valor_total"], 2),
        "score_medio":        round(sum(scores) / len(scores), 2) if scores else None,
        "ordem":              pipeline_meta.get("ordem"),
        "categoria":          pipeline_meta.get("categoria"),
        "prob_fechamento":    pipeline_meta.get("probabilidade_fechamento"),
    }

# ── 2. Conversion rates between consecutive stages ──
# Only for canonical pipeline stages in order
ETAPAS_FUNIL_ORDER = [
    ("Novo Lead", 1),
    ("Contato Feito", 2),
    ("Reunião marcada", 3),
    ("Proposta Enviada", 4),
    ("Negociação", 5),
    ("Fechado Ganho", 6),
]

conversion_rates = {}
counts_by_etapa = {e: funnel_data.get(e, {}).get("count", 0) for e, _ in ETAPAS_FUNIL_ORDER}

for i in range(len(ETAPAS_FUNIL_ORDER) - 1):
    etapa_from, _ = ETAPAS_FUNIL_ORDER[i]
    etapa_to, _ = ETAPAS_FUNIL_ORDER[i + 1]
    from_count = counts_by_etapa.get(etapa_from, 0)
    to_count = counts_by_etapa.get(etapa_to, 0)
    rate = round(to_count / from_count * 100, 2) if from_count > 0 else None
    conversion_rates[f"{etapa_from} → {etapa_to}"] = {
        "de":              etapa_from,
        "para":            etapa_to,
        "count_de":        from_count,
        "count_para":      to_count,
        "taxa_conversao":  rate,
    }

# ── 3. Monthly volume (last 12 months) ──
monthly_volume = defaultdict(int)
cutoff_year  = 2026
cutoff_month = 6  # June 2026 = current
for lead in leads_clean:
    dt = parse_date(lead.get("data_entrada"))
    if dt:
        key = f"{dt.year}-{dt.month:02d}"
        monthly_volume[key] += 1

# Keep last 12 months relative to 2026-06
last_12 = {}
for y, m in [(2025, mo) for mo in range(7, 13)] + [(2026, mo) for mo in range(1, 7)]:
    key = f"{y}-{m:02d}"
    last_12[key] = monthly_volume.get(key, 0)

# ── 4. Lost/Won analysis ──
lost_leads = [l for l in leads_clean if l.get("etapa_funil") in ("Fechado Perdido",)]
won_leads  = [l for l in leads_clean if l.get("etapa_funil") in ("Fechado Ganho",)]

def analyse_group(group, label):
    by_canal    = Counter(l.get("canal") or "Desconhecido" for l in group)
    by_segmento = Counter(l.get("segmento") or "Desconhecido" for l in group)
    by_vendedor = Counter(l.get("responsavel") or "Sem Responsável" for l in group)
    # objeções from interactions
    objs = []
    for l in group:
        obj = l.get("interacoes", {}).get("principal_objecao")
        if obj:
            objs.append(obj)
    by_objecao = Counter(objs)
    return {
        "total":        len(group),
        "por_canal":    dict(by_canal.most_common(10)),
        "por_segmento": dict(by_segmento.most_common(10)),
        "por_vendedor": dict(by_vendedor.most_common(10)),
        "por_objecao":  dict(by_objecao.most_common(10)),
    }

lost_analysis = analyse_group(lost_leads, "perdidos")
won_analysis  = analyse_group(won_leads, "ganhos")

# ── 5. Score distribution ──
score_bands = {"0-24": 0, "25-49": 0, "50-74": 0, "75-99": 0, "sem_score": 0}
for lead in leads_clean:
    s = lead.get("score_crm")
    if s is None:
        score_bands["sem_score"] += 1
    elif s <= 24:
        score_bands["0-24"] += 1
    elif s <= 49:
        score_bands["25-49"] += 1
    elif s <= 74:
        score_bands["50-74"] += 1
    else:
        score_bands["75-99"] += 1

# ── 6. Sentiment per funnel stage ──
sentiment_by_stage = defaultdict(lambda: Counter())
for lead in leads_clean:
    etapa = lead.get("etapa_funil") or "Desconhecida"
    sent  = (lead.get("interacoes") or {}).get("sentimento_dominante")
    if sent:
        sentiment_by_stage[etapa][sent] += 1

sentiment_by_stage_out = {
    etapa: dict(counter)
    for etapa, counter in sentiment_by_stage.items()
}

# ── 7. Main objections per stage ──
objecoes_by_stage = defaultdict(lambda: Counter())
for lead in leads_clean:
    etapa = lead.get("etapa_funil") or "Desconhecida"
    obj   = (lead.get("interacoes") or {}).get("principal_objecao")
    if obj:
        objecoes_by_stage[etapa][obj] += 1

objecoes_by_stage_out = {
    etapa: dict(counter.most_common(5))
    for etapa, counter in objecoes_by_stage.items()
}

aggregated_metrics = {
    "_computed_at":        ENRICHED_AT,
    "total_leads":         total_leads,
    "funnel_summary":      funnel_summary,
    "conversion_rates":    conversion_rates,
    "monthly_volume":      last_12,
    "lost_analysis":       lost_analysis,
    "won_analysis":        won_analysis,
    "score_distribution":  score_bands,
    "sentiment_by_stage":  sentiment_by_stage_out,
    "objecoes_by_stage":   objecoes_by_stage_out,
}

# ─────────────────────────── Patterns summary ────────────────
pattern_types = Counter(p["tipo"] for p in patterns)
print(f"  Patterns registered: {len(patterns):,}")
for tipo, cnt in pattern_types.most_common():
    print(f"    {tipo}: {cnt:,}")

# ─────────────────────────── Analysis manifest ───────────────
analysis_manifest = {
    "analysed_at":         ENRICHED_AT,
    "pipeline_stage":      "analysis",
    "input_manifest":      os.path.join(INPUT_DIR, "extraction_manifest.json"),
    "status":              "success",
    "record_counts": {
        "leads_total":           stats["total"],
        "leads_com_interacoes":  stats["com_interacoes"],
        "leads_sem_interacoes":  stats["sem_interacoes"],
        "campaigns_indexadas":   len(campaigns_index),
        "interacoes_indexadas":  len(interactions_index),
        "pipeline_etapas":       len(pipeline_index),
    },
    "normalization_stats": {
        "canal_normalizado":    stats["canal_normalizado"],
        "canal_nao_mapeado":    stats["canal_nao_mapeado"],
        "etapa_normalizada":    stats["etapa_normalizada"],
        "etapa_nao_mapeada":    stats["etapa_nao_mapeada"],
        "pct_canal_ok":         round(stats["canal_normalizado"] / stats["total"] * 100, 2),
        "pct_etapa_ok":         round(stats["etapa_normalizada"] / stats["total"] * 100, 2),
    },
    "quality_stats": {
        "sem_responsavel":      stats["sem_responsavel"],
        "sem_campanha":         stats["sem_campanha"],
        "com_inconsistencias":  stats["com_inconsistencias"],
        "pct_inconsistencias":  round(stats["com_inconsistencias"] / stats["total"] * 100, 2),
    },
    "inconsistencias_por_tipo": dict(pattern_types),
    "output_files": {
        "leads_clean":          os.path.join(OUTPUT_DIR, "leads_clean.json"),
        "patterns":             os.path.join(OUTPUT_DIR, "patterns.json"),
        "aggregated_metrics":   os.path.join(OUTPUT_DIR, "aggregated_metrics.json"),
        "analysis_manifest":    os.path.join(OUTPUT_DIR, "analysis_manifest.json"),
    },
    "indexes_empty": {
        "campaigns_index":    len(campaigns_index) == 0,
        "interactions_index": len(interactions_index) == 0,
        "pipeline_index":     len(pipeline_index) == 0,
    },
}

# ─────────────────────────── Save outputs ────────────────────
print("Saving output files...")

out_leads = os.path.join(OUTPUT_DIR, "leads_clean.json")
out_patterns = os.path.join(OUTPUT_DIR, "patterns.json")
out_metrics = os.path.join(OUTPUT_DIR, "aggregated_metrics.json")
out_manifest = os.path.join(OUTPUT_DIR, "analysis_manifest.json")

with open(out_leads, "w", encoding="utf-8") as f:
    json.dump(leads_clean, f, ensure_ascii=False, indent=2)
print(f"  leads_clean.json: {len(leads_clean):,} records")

with open(out_patterns, "w", encoding="utf-8") as f:
    json.dump(patterns, f, ensure_ascii=False, indent=2)
print(f"  patterns.json: {len(patterns):,} records")

with open(out_metrics, "w", encoding="utf-8") as f:
    json.dump(aggregated_metrics, f, ensure_ascii=False, indent=2)
print(f"  aggregated_metrics.json: saved")

with open(out_manifest, "w", encoding="utf-8") as f:
    json.dump(analysis_manifest, f, ensure_ascii=False, indent=2)
print(f"  analysis_manifest.json: saved")

# ─────────────────────────── Final report ────────────────────
print("\n" + "="*60)
print("PIPELINE STAGE 2 - ANALYSIS COMPLETE")
print("="*60)
print(json.dumps(analysis_manifest, ensure_ascii=False, indent=2))
