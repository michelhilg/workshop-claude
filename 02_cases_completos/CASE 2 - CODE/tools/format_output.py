import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / ".claude" / "agents" / "padronizador" / "config.json"


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_json(path, default=None):
    if not Path(path).exists():
        if default is not None:
            return default
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def load_config():
    cfg = load_json(CONFIG_PATH)
    cfg["input_dir"] = PROJECT_ROOT / cfg["input_dir"]
    cfg["output_dir"] = PROJECT_ROOT / cfg["output_dir"]
    return cfg


# ---------------------------------------------------------------------------
# Value helpers
# ---------------------------------------------------------------------------

def safe_float(v, default=0.0):
    try:
        return float(v) if v not in (None, "", "null") else default
    except (TypeError, ValueError):
        return default


def safe_int(v, default=0):
    try:
        return int(float(v)) if v not in (None, "", "null") else default
    except (TypeError, ValueError):
        return default


def fmt_currency(value, symbol="R$", decimals=2):
    return f"{symbol} {value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def days_since(date_str):
    if not date_str:
        return None
    try:
        dt = datetime.fromisoformat(str(date_str).replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - dt.astimezone(timezone.utc)
        return delta.days
    except Exception:
        return None


def responsavel(lead):
    return lead.get("responsavel") or lead.get("owner") or lead.get("vendedor")


def etapa(lead):
    return lead.get("etapa_funil") or ""


def is_perdido(e):
    return str(e).lower() in {"fechado perdido", "perdido", "lost"}


def is_ganho(e):
    return str(e).lower() in {"fechado ganho", "ganho", "won"}


# ---------------------------------------------------------------------------
# 1. pipeline_view.json
# ---------------------------------------------------------------------------

def build_pipeline_view(leads, cfg):
    funil_order = {s: i for i, s in enumerate(cfg["funil_order"])}
    fields = cfg["pipeline_lead_fields"]

    groups = defaultdict(list)
    for lead in leads:
        groups[etapa(lead)].append(lead)

    stages = []
    for stage_name, stage_leads in groups.items():
        order = funil_order.get(stage_name, 99)
        valores = [safe_float(l.get("valor_estimado") or l.get("value")) for l in stage_leads]
        scores = [safe_int(l.get("score")) for l in stage_leads if l.get("score")]
        prob = stage_leads[0].get("_probabilidade_fechamento") if stage_leads else None
        categoria = stage_leads[0].get("_etapa_categoria") if stage_leads else None

        slim_leads = [{f: l.get(f) for f in fields} for l in stage_leads]

        stages.append({
            "etapa": stage_name,
            "ordem": order,
            "categoria": categoria,
            "probabilidade_fechamento": prob,
            "total_leads": len(stage_leads),
            "valor_total": round(sum(valores), 2),
            "score_medio": round(sum(scores) / len(scores), 1) if scores else None,
            "leads": slim_leads,
        })

    stages.sort(key=lambda x: x["ordem"])
    return stages


# ---------------------------------------------------------------------------
# 2. channel_performance.json
# ---------------------------------------------------------------------------

def build_channel_performance(leads):
    groups = defaultdict(list)
    for lead in leads:
        canal = lead.get("canal") or "Desconhecido"
        groups[canal].append(lead)

    result = []
    for canal, canal_leads in groups.items():
        valores = [safe_float(l.get("valor_estimado") or l.get("value")) for l in canal_leads]
        scores = [safe_int(l.get("score")) for l in canal_leads if l.get("score")]
        etapas = Counter(etapa(l) for l in canal_leads)
        result.append({
            "canal": canal,
            "total_leads": len(canal_leads),
            "valor_total": round(sum(valores), 2),
            "valor_medio": round(sum(valores) / len(valores), 2) if valores else 0,
            "score_medio": round(sum(scores) / len(scores), 1) if scores else None,
            "distribuicao_etapas": dict(etapas.most_common()),
        })

    result.sort(key=lambda x: x["total_leads"], reverse=True)
    return result


# ---------------------------------------------------------------------------
# 3. seller_performance.json
# ---------------------------------------------------------------------------

def build_seller_performance(leads):
    groups = defaultdict(list)
    for lead in leads:
        resp = responsavel(lead) or "Sem responsável"
        groups[resp].append(lead)

    result = []
    for resp, resp_leads in groups.items():
        valores = [safe_float(l.get("valor_estimado") or l.get("value")) for l in resp_leads]
        scores = [safe_int(l.get("score")) for l in resp_leads if l.get("score")]
        etapas = Counter(etapa(l) for l in resp_leads)
        ganhos = sum(1 for l in resp_leads if is_ganho(etapa(l)))
        perdidos = sum(1 for l in resp_leads if is_perdido(etapa(l)))
        result.append({
            "responsavel": resp,
            "total_leads": len(resp_leads),
            "valor_total": round(sum(valores), 2),
            "score_medio": round(sum(scores) / len(scores), 1) if scores else None,
            "ganhos": ganhos,
            "perdidos": perdidos,
            "distribuicao_etapas": dict(etapas.most_common()),
        })

    result.sort(key=lambda x: x["total_leads"], reverse=True)
    return result


# ---------------------------------------------------------------------------
# 4. campaign_performance.json
# ---------------------------------------------------------------------------

def build_campaign_performance(leads):
    groups = defaultdict(list)
    for lead in leads:
        cid = str(lead.get("campanha_id") or lead.get("campaign_id") or "sem_campanha")
        groups[cid].append(lead)

    result = []
    for cid, camp_leads in groups.items():
        valores = [safe_float(l.get("valor_estimado") or l.get("value")) for l in camp_leads]
        ganhos = sum(1 for l in camp_leads if is_ganho(etapa(l)))
        perdidos = sum(1 for l in camp_leads if is_perdido(etapa(l)))
        total = len(camp_leads)
        win_rate = round(ganhos / total * 100, 2) if total else 0
        valor_total = round(sum(valores), 2)
        sample = camp_leads[0]
        investimento = safe_float(sample.get("_campanha_investimento") or sample.get("investimento"))
        roi = round((valor_total / investimento - 1) * 100, 2) if investimento else None
        etapas = Counter(etapa(l) for l in camp_leads)
        result.append({
            "campanha_id": cid,
            "campanha_nome": sample.get("_campanha_nome"),
            "canal": sample.get("_campanha_canal"),
            "objetivo": sample.get("_campanha_objetivo"),
            "total_leads": total,
            "valor_total": valor_total,
            "valor_medio": round(valor_total / total, 2) if total else 0,
            "ganhos": ganhos,
            "perdidos": perdidos,
            "win_rate_pct": win_rate,
            "roi_pct": roi,
            "distribuicao_etapas": dict(etapas.most_common()),
        })

    result.sort(key=lambda x: x["total_leads"], reverse=True)
    return result


# ---------------------------------------------------------------------------
# 5. alerts.json
# ---------------------------------------------------------------------------

def build_alerts(leads, cfg):
    alert_cfg = cfg["alerts"]
    sem_interacao_dias = alert_cfg["sem_interacao_dias"]
    parado_qualificado_dias = alert_cfg["parado_qualificado_dias"]
    etapas_avancadas = set(alert_cfg["etapas_avancadas"])
    gargalo_queda = alert_cfg["gargalo_queda_percentual"]
    funil_order = cfg["funil_order"]

    alerts = []

    # Leads sem responsável
    sem_resp = [l for l in leads if not responsavel(l)]
    if sem_resp:
        alerts.append({
            "tipo": "sem_responsavel",
            "severidade": "alta",
            "mensagem": f"{len(sem_resp)} lead(s) sem responsável atribuído",
            "count": len(sem_resp),
            "lead_ids": [l.get("lead_id") or l.get("id") for l in sem_resp[:20]],
        })

    # Leads em etapas avançadas sem interação há mais de N dias
    parados_avancados = []
    for lead in leads:
        if etapa(lead) in etapas_avancadas:
            dias = days_since(lead.get("_ultima_interacao"))
            if dias is not None and dias > sem_interacao_dias:
                parados_avancados.append({
                    "lead_id": lead.get("lead_id") or lead.get("id"),
                    "nome": lead.get("nome"),
                    "etapa": etapa(lead),
                    "dias_sem_interacao": dias,
                    "responsavel": responsavel(lead),
                })
    if parados_avancados:
        parados_avancados.sort(key=lambda x: x["dias_sem_interacao"], reverse=True)
        alerts.append({
            "tipo": "parado_etapa_avancada",
            "severidade": "alta",
            "mensagem": f"{len(parados_avancados)} lead(s) em etapas avançadas sem interação há mais de {sem_interacao_dias} dias",
            "count": len(parados_avancados),
            "leads": parados_avancados[:20],
        })

    # Leads parados em "Qualificado" há mais de N dias
    parados_qualif = []
    for lead in leads:
        if str(etapa(lead)).lower() in {"qualificado", "qualificação"}:
            dias = days_since(lead.get("_ultima_interacao") or lead.get("data_entrada"))
            if dias is not None and dias > parado_qualificado_dias:
                parados_qualif.append({
                    "lead_id": lead.get("lead_id") or lead.get("id"),
                    "nome": lead.get("nome"),
                    "dias_parado": dias,
                    "responsavel": responsavel(lead),
                })
    if parados_qualif:
        parados_qualif.sort(key=lambda x: x["dias_parado"], reverse=True)
        alerts.append({
            "tipo": "parado_qualificado",
            "severidade": "media",
            "mensagem": f"{len(parados_qualif)} lead(s) parado(s) em 'Qualificado' há mais de {parado_qualificado_dias} dias",
            "count": len(parados_qualif),
            "leads": parados_qualif[:20],
        })

    # Gargalo: queda > N% de "Reunião marcada" para "Proposta Enviada"
    etapa_counts = Counter(etapa(l) for l in leads)
    reuniao = etapa_counts.get("Reunião marcada", 0)
    proposta = etapa_counts.get("Proposta Enviada", 0)
    if reuniao > 0:
        queda = (reuniao - proposta) / reuniao * 100
        if queda > gargalo_queda:
            alerts.append({
                "tipo": "gargalo_funil",
                "severidade": "media",
                "mensagem": f"Gargalo detectado: queda de {queda:.1f}% de 'Reunião marcada' ({reuniao}) para 'Proposta Enviada' ({proposta})",
                "reuniao_marcada": reuniao,
                "proposta_enviada": proposta,
                "queda_pct": round(queda, 1),
            })

    return sorted(alerts, key=lambda x: {"alta": 0, "media": 1}.get(x["severidade"], 2))


# ---------------------------------------------------------------------------
# 6. data_quality_report.json
# ---------------------------------------------------------------------------

def build_data_quality_report(leads, patterns):
    total = len(leads)
    canal_ok = sum(1 for l in leads if l.get("_canal_normalizado"))
    etapa_ok = sum(1 for l in leads if l.get("_etapa_normalizada"))
    sem_resp = sum(1 for l in leads if not responsavel(l))
    sem_camp = sum(1 for l in leads if not l.get("_campanha_encontrada"))

    tipos = Counter(p["tipo"] for p in patterns)
    canais_nao_mapeados = sorted({
        p.get("valor_original") or p.get("valor") for p in patterns if p["tipo"] == "canal_nao_mapeado" and (p.get("valor_original") or p.get("valor"))
    })
    etapas_nao_mapeadas = sorted({
        p.get("valor_original") or p.get("valor") for p in patterns if p["tipo"] == "etapa_nao_mapeada" and (p.get("valor_original") or p.get("valor"))
    })

    return {
        "total_leads": total,
        "normalizacao_canal": {
            "normalizados": canal_ok,
            "nao_mapeados": total - canal_ok,
            "taxa_pct": round(canal_ok / total * 100, 1) if total else 0,
            "valores_nao_mapeados": canais_nao_mapeados,
        },
        "normalizacao_etapa": {
            "normalizados": etapa_ok,
            "nao_mapeados": total - etapa_ok,
            "taxa_pct": round(etapa_ok / total * 100, 1) if total else 0,
            "valores_nao_mapeados": etapas_nao_mapeadas,
        },
        "leads_sem_responsavel": sem_resp,
        "leads_sem_campanha": sem_camp,
        "inconsistencias_por_tipo": dict(tipos),
        "total_inconsistencias": len(patterns),
    }


# ---------------------------------------------------------------------------
# 7. leads_table.json
# ---------------------------------------------------------------------------

def build_leads_table(leads, cfg):
    fields = cfg["leads_table_fields"]
    table = []
    for lead in leads:
        row = {f: lead.get(f) for f in fields if f in lead or True}
        table.append(row)
    return table


# ---------------------------------------------------------------------------
# 8. dashboard_summary.json
# ---------------------------------------------------------------------------

def build_dashboard_summary(leads, alerts, channel_perf, seller_perf, pipeline_view, cfg):
    top_n = cfg["top_n"]
    top_alerts_n = cfg["top_alerts"]
    top_rec_n = cfg["top_recommendations"]

    total = len(leads)
    valores = [safe_float(l.get("valor_estimado") or l.get("value")) for l in leads]
    scores = [safe_int(l.get("score")) for l in leads if l.get("score")]
    sem_resp = sum(1 for l in leads if not responsavel(l))
    valor_total = round(sum(valores), 2)

    # Conversões por etapa (counts)
    stage_counts = {s["etapa"]: s["total_leads"] for s in pipeline_view}

    # Receita em risco: leads em negociação sem interação recente
    receita_risco = sum(
        safe_float(l.get("valor_estimado"))
        for l in leads
        if str(etapa(l)).lower() == "negociação"
        and (days_since(l.get("_ultima_interacao")) or 0) > 14
    )

    return {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "total_leads": total,
        "valor_total": valor_total,
        "score_medio": round(sum(scores) / len(scores), 1) if scores else None,
        "leads_sem_responsavel": sem_resp,
        "receita_em_risco": round(receita_risco, 2),
        "top_canais": [
            {"canal": c["canal"], "total_leads": c["total_leads"], "valor_total": c["valor_total"]}
            for c in channel_perf[:top_n]
        ],
        "top_vendedores": [
            {"responsavel": s["responsavel"], "total_leads": s["total_leads"], "ganhos": s["ganhos"]}
            for s in seller_perf[:top_n]
            if s["responsavel"] != "Sem responsável"
        ][:top_n],
        "conversoes_por_etapa": stage_counts,
        "top_alertas": [
            {"tipo": a["tipo"], "severidade": a["severidade"], "mensagem": a["mensagem"]}
            for a in alerts[:top_alerts_n]
        ],
    }


# ---------------------------------------------------------------------------
# 9. recommendations.json
# ---------------------------------------------------------------------------

def build_recommendations(insights, cfg):
    top_n = cfg["top_recommendations"]
    if not insights:
        return {"alta": [], "media": [], "baixa": []}

    recs = insights if isinstance(insights, list) else insights.get("recommendations", [])
    alta = [r for r in recs if str(r.get("prioridade") or r.get("priority") or "").lower() == "alta"]
    media = [r for r in recs if str(r.get("prioridade") or r.get("priority") or "").lower() == "média" or
             str(r.get("prioridade") or r.get("priority") or "").lower() == "media"]
    baixa = [r for r in recs if r not in alta and r not in media]

    return {
        "alta": alta[:top_n],
        "media": media[:top_n],
        "baixa": baixa[:top_n],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        cfg = load_config()
    except FileNotFoundError:
        print(f"ERRO: config.json não encontrado em {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    input_dir = cfg["input_dir"]
    output_dir = cfg["output_dir"]

    # Check precondition
    manifest_in = input_dir / "analysis_manifest.json"
    if not manifest_in.exists():
        print(
            "ERRO: analysis_manifest.json não encontrado. "
            "O agente analista precisa rodar primeiro.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load inputs
    print("\nCarregando dados de entrada...")
    leads = load_json(input_dir / "leads_clean.json")
    patterns = load_json(input_dir / "patterns.json", default=[])
    insights = load_json(input_dir / "insights.json", default=[])
    print(f"  {len(leads)} leads carregados | {len(patterns)} inconsistências | insights: {'sim' if insights else 'não'}")

    generated_at = datetime.now(timezone.utc).isoformat()
    manifest_entries = []

    def write(filename, data):
        path = output_dir / filename
        save_json(path, data)
        size_kb = round(path.stat().st_size / 1024, 1)
        count = len(data) if isinstance(data, list) else None
        manifest_entries.append({
            "arquivo": filename,
            "status": "success",
            "tamanho_kb": size_kb,
            "registros": count,
        })
        label = f"{count} registros" if count is not None else f"{size_kb} KB"
        print(f"  ✓ {filename:<35} {label}")

    print(f"\nGerando outputs em .claude/data/output/\n{'─' * 55}")

    pipeline_view = build_pipeline_view(leads, cfg)
    write("pipeline_view.json", pipeline_view)

    channel_perf = build_channel_performance(leads)
    write("channel_performance.json", channel_perf)

    seller_perf = build_seller_performance(leads)
    write("seller_performance.json", seller_perf)

    write("campaign_performance.json", build_campaign_performance(leads))

    alerts = build_alerts(leads, cfg)
    write("alerts.json", alerts)

    write("data_quality_report.json", build_data_quality_report(leads, patterns))

    write("leads_table.json", build_leads_table(leads, cfg))

    summary = build_dashboard_summary(leads, alerts, channel_perf, seller_perf, pipeline_view, cfg)
    write("dashboard_summary.json", summary)

    write("recommendations.json", build_recommendations(insights, cfg))

    # Manifest
    output_manifest = {
        "generated_at": generated_at,
        "total_arquivos": len(manifest_entries),
        "arquivos": manifest_entries,
        "status": "success",
    }
    save_json(output_dir / "output_manifest.json", output_manifest)

    print(f"{'─' * 55}")
    print(f"  output_manifest.json gerado")
    print(f"\n  Total de leads:        {summary['total_leads']}")
    print(f"  Valor total:           {fmt_currency(summary['valor_total'], cfg['currency_symbol'], cfg['decimal_places'])}")
    print(f"  Alertas operacionais:  {len(alerts)}")
    print(f"  Leads sem responsável: {summary['leads_sem_responsavel']}")
    print(f"\nFormatação concluída — {len(manifest_entries)}/9 arquivos gerados.")


if __name__ == "__main__":
    main()
