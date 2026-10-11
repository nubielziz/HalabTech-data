# HalabTech supply-chain research (OSINT), Rounds 1–7

This is a public-source investigation of who supplies the GSM wholesale server **HalabTech** (server.halabtech.com,
support.halabtech.com). Verification date: **2026-10-11**.

## Deliverables

| File | What it is |
|---|---|
| `HalabTech_Complete_Supply_Chain_Research.xlsx` | Research database, 28 sheets: **11 Round-7 sheets first**, then the 17 Rounds 1–6 sheets, unchanged |
| `reports/HalabTech_R7_Investigation_Summary.md` | **Round 7 summary**: answers to the 7 mission questions, with an Arabic summary block |
| `reports/NEXT_RESEARCH_MISSION_R8.md` | Next round: questions, methods, completion criteria |
| `reports/HalabTech_Report_R4-R6_AR.md` | Arabic research report for Rounds 4–6 |
| `reports/supply_chain_graph_R6.png` / `.mmd` | Supply-chain graph as of Round 6 |
| `reports/NEXT_RESEARCH_MISSION_R7.md` | Mission prepared after Round 6 |
| `reports/prior/HalabTech_Report_R1-R3.md` | Previous report (Rounds 1–3), unchanged |

## Workbook sheets

**Round 7 (new):**
1. Research Progress Dashboard (metrics with explicit formulas)
2. Complete Service Inventory (1,455 SKUs)
3. Supplier Intelligence
4. Confirmed Supply Chains
5. Suspected Supply Chains
6. Website & Public API Findings
7. Evidence Registry (EV-001…EV-491 + NEG-001…NEG-198)
8. Unresolved Cases
9. Confidence Change Log (CL-022…CL-048)
10. R7 Price Forensics
11. R7 MCP Tool Log

**Rounds 1–6 (unchanged):**
- Dashboard · All Services · Service Groups · Original Vendors
- Suppliers and Distributors · Supply Chain Relationships · Evidence Register · Unknown Suppliers
- Research Gaps · Research History · Website Inventory · Conflicts and Corrections
- Next Research Plan · Price Comparison · MCP Tool Log · Progress R3 vs R6 · R1-3 Sources

## Headline results (Round 7)

**Coverage, attribution and verification** (out of 383 groups and 1,455 SKUs):

| Measure | R6 | R7 |
|---|---|---|
| Coverage (groups checked at least once) | 30.8% | **89.3%** (342 groups) |
| Attribution (SKUs with upstream ≥LIKELY) | 27.5% | **41.3%** (601 SKUs) |
| Verification (CONFIRMED immediate source) | – | **1.4%** (21 SKUs, in-house only) |

**Named third-party supplier proven for a specific service:** 0. HalabTech's own labels show at least 4 numbered, unnamed IMEI sources.

**STRONG:**
- Sigma → GsmServer → HalabTech (exclusive distributor; panel credits bought on GsmServer).
- Chimera → GsmEasy, GsmServer or Unlock.eu → HalabTech.
- Hunter Unlocker, Q-Unlocker and XTP → HalabTech (direct).
- "GsmServer Products" group, 2020–2024.

**LIKELY:**
- Fast Unlocking (UMT/NCK/Avengers)
- GSM Nigeria (Alseery, F-KEY)
- Cerberus (vendor DHRU API)
- GSMFATHER (Moldova)
- GsmDone (GsmAuth)
- GsmEasy (SETool)
- AppleUnlockers (CF Tools)
- ADY Unlocker (Tira, TheMagicTool, GuerraTool, Panda)

**Reversed or disputed:**
- UnlocksPro is a HalabTech customer, not a supplier.
- Code-GSM is a HalabTech customer for the Mi Account family.
- Code-GSM's role for T-Mobile Clean & Paid Off is DISPUTED.

**Vendor listings:** 125 developers list HalabTech (62 in R6). A listing proves an authorised channel, not an API connection.

## Repository layout

```
data/catalog/      parsed public catalog, 02:00 UTC (Rounds 4-6)
data/raw/          Rounds 4-6 page captures
data/findings/     Rounds 4-6 findings (OWN, A1, A2, B, C, D, V)
data/reference/    Rounds 1-3 tables; curated Rounds 4-6 dataset
data/r7/           Round 7: brief, findings W1-W7 + V7 (raw, unmodified), raw captures and 10:03/10:39 UTC
                   catalog snapshots, price forensics, r7_metrics.json (W6 derived parses omitted; regenerable)
scripts/           Rounds 4-6 pipeline (rebuild.sh -> build/r6)
scripts/r7/        Round 7 pipeline: curate_r7_data.py (curated knowledge + Phase-5 corrections), curate_r7.py
                   (engine + metrics), build_r7.py (adds sheets, never edits R1-R6 sheets), rebuild_r7.sh; streams/ = as-run
                   stream scripts (paths refer to the original workspace)
```

`scripts/r7/rebuild_r7.sh [out.xlsx]` regenerates the current workbook from the committed data without network access. It was verified to reproduce all 28 sheets with 0 differing rows.

## Evidence rules used

- A vendor listing proves an authorised channel only, not an API connection.
- Identical service names or similar prices are leads only.
- HalabTech dealers sell 2.8–12.5% below HalabTech's list, so "cheaper" does not mean "upstream".
- "Miniutes" is a Dhru default, not a fingerprint.
- Confidence scale: CONFIRMED / STRONG / LIKELY / UNKNOWN / DISPUTED.
- Only public pages and public files were accessed. No logins, no private endpoints, no chatbot prompting.
- Tokens seen in captured public HTML (store CSRF, chat-widget key) are redacted.
