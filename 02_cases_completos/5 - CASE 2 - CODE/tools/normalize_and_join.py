import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / ".claude" / "agents" / "analista" / "config.json"


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


# ---------------------------------------------------------------------------
# Config & paths
# ---------------------------------------------------------------------------

def load_config():
    cfg = load_json(CONFIG_PATH)
    cfg["input_dir"] = PROJECT_ROOT / cfg["input_dir"]
    cfg["output_dir"] = PROJECT_ROOT / cfg["output_dir"]
    return cfg


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def normalize(value, mapping):
    if not value:
        return None, False
    canonical = mapping.get(str(value).strip())
    if canonical:
        return canonical, True
    # Case-insensitive fallback
    lower = str(value).strip().lower()
    for k, v in mapping.items():
        if k.lower() == lower:
            return v, True
    return str(value).strip(), False


# ---------------------------------------------------------------------------
# Index builders
# ---------------------------------------------------------------------------

def build_campaigns_index(campaigns):
    return {str(c.get("campanha_id", c.get("id", ""))): c for c in campaigns}


def _moda(values):
    filtered = [v for v in values if v]
    if not filtered:
        return None
    return Counter(filtered).most_common(1)[0][0]


def build_interactions_index(interactions):
    groups = defaultdict(list)
    for row in interactions:
        lid = str(row.get("lead_id", ""))
        if lid:
            groups[lid].append(row)

    index = {}
    for lead_id, rows in groups.items():
        dates = [r.get("data_interacao") or r.get("date") or r.get("data") for r in rows]
        dates = sorted([d for d in dates if d], reverse=True)
        index[lead_id] = {
            "total_interacoes": len(rows),
            "ultima_interacao": dates[0] if dates else None,
            "sentimento_dominante": _moda(
                [r.get("sentimento") or r.get("sentiment") for r in rows]
            ),
            "principal_objecao": _moda(
                [r.get("objecao") or r.get("objection") or r.get("objeção") for r in rows]
            ),
        }
    return index


def build_pipeline_index(pipeline_config):
    index = {}
    for row in pipeline_config:
        key = row.get("etapa_funil") or row.get("etapa") or row.get("stage") or ""
        if key:
            index[str(key).strip()] = {
                "ordem": row.get("ordem") or row.get("order"),
                "categoria": row.get("categoria") or row.get("category"),
                "probabilidade_fechamento": row.get("probabilidade_fechamento")
                    or row.get("probabilidade")
                    or row.get("win_rate"),
            }
    return index


# ---------------------------------------------------------------------------
# Lead enrichment
# ---------------------------------------------------------------------------

def enrich_lead(lead, canal_map, etapa_map, camp_idx, inter_idx, pipe_idx, enriched_at):
    record = dict(lead)

    # Normalize canal
    raw_canal = record.get("canal") or record.get("channel") or ""
    canal_norm, canal_ok = normalize(raw_canal, canal_map)
    record["canal"] = canal_norm
    record["_canal_original"] = raw_canal
    record["_canal_normalizado"] = canal_ok

    # Normalize etapa
    raw_etapa = record.get("etapa_funil") or record.get("etapa") or record.get("stage") or ""
    etapa_norm, etapa_ok = normalize(raw_etapa, etapa_map)
    record["etapa_funil"] = etapa_norm
    record["_etapa_original"] = raw_etapa
    record["_etapa_normalizada"] = etapa_ok

    # Join campaigns
    cid = str(record.get("campanha_id") or record.get("campaign_id") or "")
    camp_data = camp_idx.get(cid, {})
    record["_campanha_nome"] = camp_data.get("nome") or camp_data.get("name")
    record["_campanha_canal"] = camp_data.get("canal") or camp_data.get("channel")
    record["_campanha_objetivo"] = camp_data.get("objetivo") or camp_data.get("objective")
    record["_campanha_encontrada"] = bool(camp_data)

    # Join interactions
    lid = str(record.get("lead_id") or record.get("id") or "")
    inter_data = inter_idx.get(lid, {})
    record["_total_interacoes"] = inter_data.get("total_interacoes", 0)
    record["_ultima_interacao"] = inter_data.get("ultima_interacao")
    record["_sentimento_dominante"] = inter_data.get("sentimento_dominante")
    record["_principal_objecao"] = inter_data.get("principal_objecao")

    # Join pipeline
    pipe_data = pipe_idx.get(etapa_norm, {})
    record["_etapa_ordem"] = pipe_data.get("ordem")
    record["_etapa_categoria"] = pipe_data.get("categoria")
    record["_probabilidade_fechamento"] = pipe_data.get("probabilidade_fechamento")

    record["_enriched_at"] = enriched_at
    return record


# ---------------------------------------------------------------------------
# Patterns (inconsistencies)
# ---------------------------------------------------------------------------

def collect_patterns(enriched_leads):
    patterns = []
    for lead in enriched_leads:
        lid = lead.get("lead_id") or lead.get("id")
        if not lead.get("_canal_normalizado"):
            patterns.append({
                "lead_id": lid,
                "tipo": "canal_nao_mapeado",
                "valor": lead.get("_canal_original"),
            })
        if not lead.get("_etapa_normalizada"):
            patterns.append({
                "lead_id": lid,
                "tipo": "etapa_nao_mapeada",
                "valor": lead.get("_etapa_original"),
            })
        responsavel = lead.get("responsavel") or lead.get("owner") or lead.get("vendedor")
        if not responsavel:
            patterns.append({"lead_id": lid, "tipo": "sem_responsavel", "valor": None})
        if not lead.get("_campanha_encontrada"):
            patterns.append({
                "lead_id": lid,
                "tipo": "sem_campanha",
                "valor": lead.get("campanha_id") or lead.get("campaign_id"),
            })
    return patterns


# ---------------------------------------------------------------------------
# Aggregated metrics
# ---------------------------------------------------------------------------

def safe_float(v):
    try:
        return float(v) if v not in (None, "", "null") else 0.0
    except (TypeError, ValueError):
        return 0.0


def safe_int(v):
    try:
        return int(float(v)) if v not in (None, "", "null") else 0
    except (TypeError, ValueError):
        return 0


def compute_metrics(enriched_leads, pipe_idx):
    total = len(enriched_leads)

    # --- Funnel summary ---
    funnel_counts = Counter()
    funnel_value = defaultdict(float)
    funnel_scores = defaultdict(list)
    for lead in enriched_leads:
        etapa = lead.get("etapa_funil") or "Não mapeada"
        funnel_counts[etapa] += 1
        funnel_value[etapa] += safe_float(lead.get("valor_estimado") or lead.get("value"))
        score = safe_int(lead.get("score"))
        if score:
            funnel_scores[etapa].append(score)

    funnel_summary = {}
    for etapa, count in funnel_counts.items():
        scores = funnel_scores[etapa]
        funnel_summary[etapa] = {
            "contagem": count,
            "percentual": round(count / total * 100, 2) if total else 0,
            "valor_total": round(funnel_value[etapa], 2),
            "score_medio": round(sum(scores) / len(scores), 1) if scores else None,
        }

    # --- Conversion rates between consecutive stages ---
    ordered_stages = sorted(
        [(k, v.get("ordem") or 99) for k, v in pipe_idx.items()],
        key=lambda x: x[1],
    )
    conversion_rates = {}
    for i in range(len(ordered_stages) - 1):
        cur, _ = ordered_stages[i]
        nxt, _ = ordered_stages[i + 1]
        cur_count = funnel_counts.get(cur, 0)
        nxt_count = funnel_counts.get(nxt, 0)
        conversion_rates[f"{cur} → {nxt}"] = (
            round(nxt_count / cur_count * 100, 2) if cur_count else None
        )

    # --- Monthly volume (last 12 months) ---
    monthly = defaultdict(int)
    for lead in enriched_leads:
        date_str = lead.get("data_entrada") or lead.get("created_at") or lead.get("data")
        if date_str:
            try:
                month = str(date_str)[:7]  # "YYYY-MM"
                monthly[month] += 1
            except Exception:
                pass
    all_months = sorted(monthly.keys(), reverse=True)[:12]
    monthly_volume = {m: monthly[m] for m in sorted(all_months)}

    # --- Won/lost analysis ---
    perdido_keywords = {"fechado perdido", "perdido", "lost"}
    ganho_keywords = {"fechado ganho", "ganho", "won"}

    def is_perdido(e):
        return str(e).lower() in perdido_keywords

    def is_ganho(e):
        return str(e).lower() in ganho_keywords

    won_lost = {
        "por_canal": {"ganhos": Counter(), "perdidos": Counter()},
        "por_segmento": {"ganhos": Counter(), "perdidos": Counter()},
        "por_vendedor": {"ganhos": Counter(), "perdidos": Counter()},
        "por_objecao": {"perdidos": Counter()},
    }
    for lead in enriched_leads:
        etapa = str(lead.get("etapa_funil") or "").lower()
        canal = lead.get("canal") or "Desconhecido"
        segmento = lead.get("segmento") or lead.get("segment") or "Desconhecido"
        vendedor = lead.get("responsavel") or lead.get("owner") or lead.get("vendedor") or "Desconhecido"
        objecao = lead.get("_principal_objecao") or "Nenhuma"
        if is_ganho(etapa):
            won_lost["por_canal"]["ganhos"][canal] += 1
            won_lost["por_segmento"]["ganhos"][segmento] += 1
            won_lost["por_vendedor"]["ganhos"][vendedor] += 1
        if is_perdido(etapa):
            won_lost["por_canal"]["perdidos"][canal] += 1
            won_lost["por_segmento"]["perdidos"][segmento] += 1
            won_lost["por_vendedor"]["perdidos"][vendedor] += 1
            won_lost["por_objecao"]["perdidos"][objecao] += 1

    # Serialize Counters
    for group in won_lost.values():
        for k in list(group.keys()):
            group[k] = dict(group[k].most_common(20))

    # --- Score distribution ---
    score_dist = {"0-24": 0, "25-49": 0, "50-74": 0, "75-99": 0}
    for lead in enriched_leads:
        s = safe_int(lead.get("score"))
        if s < 25:
            score_dist["0-24"] += 1
        elif s < 50:
            score_dist["25-49"] += 1
        elif s < 75:
            score_dist["50-74"] += 1
        else:
            score_dist["75-99"] += 1

    # --- Sentiment by stage ---
    sentiment_by_stage = defaultdict(Counter)
    for lead in enriched_leads:
        etapa = lead.get("etapa_funil") or "Não mapeada"
        sentimento = lead.get("_sentimento_dominante")
        if sentimento:
            sentiment_by_stage[etapa][sentimento] += 1
    sentiment_by_stage = {k: dict(v.most_common()) for k, v in sentiment_by_stage.items()}

    # --- Top objections by stage ---
    objections_by_stage = defaultdict(Counter)
    for lead in enriched_leads:
        etapa = lead.get("etapa_funil") or "Não mapeada"
        objecao = lead.get("_principal_objecao")
        if objecao:
            objections_by_stage[etapa][objecao] += 1
    objections_by_stage = {k: dict(v.most_common(10)) for k, v in objections_by_stage.items()}

    return {
        "funil_por_etapa": funnel_summary,
        "taxas_conversao": conversion_rates,
        "volume_mensal": monthly_volume,
        "won_lost": won_lost,
        "distribuicao_score": score_dist,
        "sentimento_por_etapa": sentiment_by_stage,
        "objecoes_por_etapa": objections_by_stage,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        config = load_config()
    except FileNotFoundError:
        print(f"ERRO: config.json não encontrado em {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    input_dir = config["input_dir"]
    output_dir = config["output_dir"]
    canal_map = config["CANAL_MAP"]
    etapa_map = config["ETAPA_MAP"]

    # Check precondition
    manifest_in = input_dir / "extraction_manifest.json"
    if not manifest_in.exists():
        print("ERRO: extraction_manifest.json não encontrado. Rode o agente extrator primeiro.", file=sys.stderr)
        sys.exit(1)

    # Load inputs
    required = ["leads_raw.json", "campaigns.json", "interactions.json", "pipeline_config.json"]
    data = {}
    for fname in required:
        path = input_dir / fname
        if not path.exists():
            print(f"ERRO: arquivo de entrada ausente: {path}", file=sys.stderr)
            sys.exit(1)
        data[fname] = load_json(path)

    print(f"\nAnálise iniciada — {len(data['leads_raw.json'])} leads carregados")
    print("─" * 50)

    # Build indices
    camp_idx = build_campaigns_index(data["campaigns.json"])
    inter_idx = build_interactions_index(data["interactions.json"])
    pipe_idx = build_pipeline_index(data["pipeline_config.json"])

    print(f"  Índice campanhas:   {len(camp_idx)} entradas")
    print(f"  Índice interações:  {len(inter_idx)} leads com histórico")
    print(f"  Índice pipeline:    {len(pipe_idx)} etapas")

    # Enrich leads
    enriched_at = datetime.now(timezone.utc).isoformat()
    enriched_leads = [
        enrich_lead(lead, canal_map, etapa_map, camp_idx, inter_idx, pipe_idx, enriched_at)
        for lead in data["leads_raw.json"]
    ]

    # Collect patterns
    patterns = collect_patterns(enriched_leads)

    # Stats
    total = len(enriched_leads)
    canal_ok = sum(1 for l in enriched_leads if l["_canal_normalizado"])
    etapa_ok = sum(1 for l in enriched_leads if l["_etapa_normalizada"])
    sem_resp = sum(
        1 for l in enriched_leads
        if not (l.get("responsavel") or l.get("owner") or l.get("vendedor"))
    )
    sem_camp = sum(1 for l in enriched_leads if not l["_campanha_encontrada"])

    # Metrics
    metrics = compute_metrics(enriched_leads, pipe_idx)

    # Save outputs
    save_json(output_dir / "leads_clean.json", enriched_leads)
    save_json(output_dir / "patterns.json", patterns)
    save_json(output_dir / "aggregated_metrics.json", metrics)

    manifest = {
        "processed_at": enriched_at,
        "total_leads": total,
        "leads_normalizados_canal": canal_ok,
        "leads_normalizados_etapa": etapa_ok,
        "leads_com_inconsistencia": len({p["lead_id"] for p in patterns}),
        "total_inconsistencias": len(patterns),
        "canais_nao_mapeados": sorted(
            {p["valor"] for p in patterns if p["tipo"] == "canal_nao_mapeado" and p["valor"]}
        ),
        "etapas_nao_mapeadas": sorted(
            {p["valor"] for p in patterns if p["tipo"] == "etapa_nao_mapeada" and p["valor"]}
        ),
        "leads_sem_responsavel": sem_resp,
        "leads_sem_campanha": sem_camp,
        "status": "success" if total > 0 else "failed",
    }
    save_json(output_dir / "analysis_manifest.json", manifest)

    # Report
    print("─" * 50)
    print(f"  Leads processados:          {total}")
    print(f"  Canal normalizado:          {canal_ok} ({canal_ok/total*100:.1f}%)")
    print(f"  Etapa normalizada:          {etapa_ok} ({etapa_ok/total*100:.1f}%)")
    print(f"  Com inconsistências:        {manifest['leads_com_inconsistencia']}")
    print(f"  Sem responsável:            {sem_resp}")
    print(f"  Sem campanha:               {sem_camp}")

    if manifest["canais_nao_mapeados"]:
        print(f"\n  Canais não mapeados:  {manifest['canais_nao_mapeados']}")
    if manifest["etapas_nao_mapeadas"]:
        print(f"  Etapas não mapeadas:  {manifest['etapas_nao_mapeadas']}")

    print("─" * 50)
    print("  Outputs salvos em .claude/data/processados/:")
    for f in ["leads_clean.json", "patterns.json", "aggregated_metrics.json", "analysis_manifest.json"]:
        size = (output_dir / f).stat().st_size / 1024 / 1024
        print(f"    ✓ {f:<30} {size:.2f} MB")

    print("\nAnálise concluída com sucesso.")


if __name__ == "__main__":
    main()
