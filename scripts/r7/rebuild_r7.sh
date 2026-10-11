#!/usr/bin/env bash
# Rebuild the Round-7 workbook from committed data (no network needed):
#   1) regenerate the Round-6 workbook with scripts/rebuild.sh into a temporary directory,
#   2) curate Round 7 (data/r7: findings W1-W7 + V7, catalog snapshots, price forensics) and
#   3) insert the 11 R7 sheets in front of the 17 preserved R1-R6 sheets.
# Usage: scripts/r7/rebuild_r7.sh [output.xlsx]   (default: the workbook in the repository root)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
bash "$REPO/scripts/rebuild.sh" "$WORK" > /dev/null
python3 "$REPO/scripts/r7/curate_r7.py" "$WORK/HalabTech_Complete_Supply_Chain_Research.xlsx" "$REPO/data/r7" "$WORK/r7_spec.json" "$WORK/r7_metrics.json" "$REPO" > /dev/null
python3 "$REPO/scripts/r7/build_r7.py" "$WORK/HalabTech_Complete_Supply_Chain_Research.xlsx" "$WORK/r7_spec.json" "${1:-$REPO/HalabTech_Complete_Supply_Chain_Research.xlsx}"
