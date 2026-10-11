# HalabTech supply-chain research (OSINT), Rounds 1–6

Public-source investigation of who supplies the GSM wholesale server **HalabTech** (server.halabtech.com,
support.halabtech.com). Verification date: **2026-10-11**.

## Deliverables

| File | What it is |
|---|---|
| `HalabTech_Complete_Supply_Chain_Research.xlsx` | Research database: 17 sheets, all Rounds 1-3 rows preserved (grey) + Rounds 4-6 additions |
| `reports/HalabTech_Report_R4-R6_AR.md` | Arabic research report (Rounds 4-6), incl. progress vs Round 3 and ranked unresolved suppliers |
| `reports/supply_chain_graph_R6.png` / `.mmd` | Supply-chain graph: solid = CONFIRMED, thick = STRONG, dashed = LIKELY, dotted/grey = UNKNOWN |
| `reports/NEXT_RESEARCH_MISSION_R7.md` | Next round: questions, queries, completion criteria, ready-to-copy prompt |
| `reports/prior/HalabTech_Report_R1-R3.md` | Previous report (Rounds 1-3), unchanged |

## Workbook sheets

Dashboard · All Services (1,489 rows: 34 R1-3 records + 1,455 public SKUs) · Service Groups (383 groups mapped to
vendor, HalabTech status, candidate upstream, confidence) · Original Vendors (VEN-000…080) · Suppliers and Distributors
(SUP-001…030) · Supply Chain Relationships (REL-001…105) · Evidence Register (EV-001…266) · Unknown Suppliers (ranked) ·
Research Gaps (GAP-001…022) · Research History · Website Inventory · Conflicts and Corrections (CL-001…021) ·
Next Research Plan · Price Comparison · MCP Tool Log · Progress R3 vs R6 · R1-3 Sources.

## Headline results (Round 6)

- Named direct API suppliers proven: **0**. HalabTech's own service names show ≥3 numbered unnamed IMEI sources.
- **STRONG**: Sigma → GsmServer (exclusive distributor) → HalabTech; Chimera → GsmEasy *or* GsmServer → HalabTech;
  Hunter Unlocker / Q-Unlocker → HalabTech (distributors-only vendors); XTP → HalabTech ("Official Main Seller").
- **LIKELY**: Code-GSM (T-Mobile "Clean & Paid Off"; price conflict on lower tiers), UnlocksPro (36 identical IMEI
  items; direction unproven), unnamed distributors for Furious Gold, UMT/NCK, Avengers, UFI, SamKey, AMT, MH Unlocker, EFT.
- 62 vendors officially list HalabTech (11 before) – this proves an authorised sales channel, not an API link.

## Repository layout

```
data/catalog/      parsed public catalog (Firecrawl scrape 2026-10-11): JSON + flat text lists
data/raw/          page captures used as evidence (live pages, vendor pages, Wayback captures 2022-2024)
data/findings/     per-stream findings with tool logs (OWN, A1, A2, B, C, D = Rounds 4-5; V = Round 6 verification)
data/reference/    Rounds 1-3 tables reconstructed from the prior report; curated Rounds 4-6 dataset
scripts/           parse_catalog.py, parse_prior.py, classify.py, curate.py, build_workbook.py, graph.py, rebuild.sh
```

`scripts/rebuild.sh [out_dir]` regenerates the workbook and graph from the committed data without network access.

## Evidence rules used

Vendor listing = authorised channel only (not an API connection). Identical service names or similar prices = leads
only (most identical strings found belong to HalabTech's own downstream customers). Confidence scale: CONFIRMED /
STRONG / LIKELY / UNKNOWN / DISPUTED. Only public pages were accessed; no logins or private supplier configurations.
