#!/usr/bin/env bash
# Rebuild the workbook and graph from the committed data (no network needed).
# Usage: scripts/rebuild.sh [output_dir]   (default: build/r6 - the repository-root workbook is the Round-7 one;
#        rebuild it with scripts/r7/rebuild_r7.sh, which calls this script first)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/raw" "$WORK/findings"
cp "$REPO"/data/catalog/server_catalog.json "$REPO"/data/catalog/imei_catalog.json "$WORK/raw/"
cp "$REPO"/data/reference/prior_sheets_R1-R3.json "$WORK/raw/prior_sheets.json"
cp "$REPO"/reports/prior/HalabTech_Report_R1-R3.md "$WORK/raw/prior_report_r1-3.md"
cp "$REPO"/data/findings/*.json "$WORK/findings/"
python3 "$REPO/scripts/curate.py" "$WORK" "$WORK/curated.json"
OUTDIR="${1:-$REPO/build/r6}"
mkdir -p "$OUTDIR/reports"
python3 "$REPO/scripts/build_workbook.py" "$WORK/raw" "$WORK/curated.json" "$OUTDIR/HalabTech_Complete_Supply_Chain_Research.xlsx"
python3 "$REPO/scripts/graph.py" "$OUTDIR/reports"
