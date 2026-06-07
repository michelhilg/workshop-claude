#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DASHBOARD_DIR="$(dirname "$SCRIPT_DIR")"
PROCESSADOS="$DASHBOARD_DIR/../.claude/data/processados"
PUBLIC_DATA="$DASHBOARD_DIR/public/data"

mkdir -p "$PUBLIC_DATA"

cp "$PROCESSADOS/aggregated_metrics.json" "$PUBLIC_DATA/"
cp "$PROCESSADOS/analysis_manifest.json" "$PUBLIC_DATA/"

echo "Dados sincronizados em $PUBLIC_DATA"
echo "  aggregated_metrics.json"
echo "  analysis_manifest.json"
