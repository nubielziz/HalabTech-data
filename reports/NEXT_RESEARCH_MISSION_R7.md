# NEXT RESEARCH MISSION — HalabTech Round 7+ (prepared 2026-10-11)

## State after Round 6
- **Confirmed:** Dhru Fusion platform; 383 public groups / 1,455 SKUs; 62 vendors officially list HalabTech; HalabTech routes IMEI orders to ≥3 numbered unnamed sources; HalabTech is a Chimera *reseller*; GsmServer resells HalabTech; HalabTech sells API access downstream.
- **STRONG:** Sigma → GsmServer → HalabTech (REL-027); Chimera → GsmEasy or GsmServer → HalabTech (REL-025); Hunter Unlocker / Q-Unlocker → HalabTech direct (REL-084); XTP → HalabTech direct (REL-085).
- **LIKELY:** Code-GSM (T-Mobile Clean & Paid Off, REL-097, price conflict CL-013); UnlocksPro (REL-098, direction unproven); unnamed distributors for Furious Gold, UMT/NCK, Avengers, UFI, SamKey, AMT, MH Unlocker, EFT (REL-086…093); GSM T-Tool / Smart Tool WW / ADY (REL-094…096); "GsmServer Products" 2022-24 (REL-028).
- **Named direct API suppliers proven:** 0.

## Questions, queries and completion criteria

| # | Question (gap) | Specific queries / URLs | Tools | Done when |
|---|---|---|---|---|
| 1 | Which Chimera distributor supplies HalabTech — GsmEasy, GsmServer or Unlock.eu? (GAP-011) | `"GsmEasy" "HalabTech"`; `site:gsmeasyshop.com chimera`; `site:imei.us halabtech`; `"chimeracredit" telegram`; compare 20k-credit reseller price GsmEasy vs GsmServer vs HalabTech 2022 ($0.101–0.112) | Parallel search, Exa search, Firecrawl scrape | One distributor named by a primary source, or two ruled out |
| 2 | Is Code-GSM HalabTech's T-Mobile source? Resolve listing-vs-detail conflict (GAP-014) | Same-day Firecrawl (`maxAge: 0`) of code-gsm.com `servicedtl/...till-xs`, `till-12-14`, `till-15`, `till-16`, `till-17` + HalabTech `/resellerpricing/imei` | Firecrawl | All 6 tiers compared on one date; markup consistent or not |
| 3 | Who copies whom: UnlocksPro or HalabTech? (GAP-015) | `web.archive.org/web/2024*/unlockspro.com/resellerpricing/imei`; `t.me/s/halabtech2?q=JDM`; `t.me/s/halabtech2?q=Signal+Labs`; first-appearance dates of "#22343" and "#26234" | Firecrawl (Wayback), Exa fetch | Dated first appearance on each side |
| 4 | Is HalabTech an iRemove partner? (GAP-016) | `"iRemove" partner DHRU`; `site:iremove.tools partner`; `gsmserver.com iremove fmi off ipad price`; `"iREMOVE FMI OFF" "WiFi Model Only" resellerpricing` (oldest server) | Parallel, Exa | Partner identified or channel ruled out |
| 5 | Price back-calculation (GAP-020): do 3-decimal prices equal candidate cost × 1.10? | HalabTech: NCK 6M $15.125, Cheetah LG $15.125, FG credit $0.878, FG pack $91.025, UMT emmc $11.875 → compare with gsmserver.com, gsmeasyshop.com, fastunlocking.com, martview.com, furiousgold.com price pages | Firecrawl, Parallel fetch | ≥3 products where cost/1.10 matches one candidate's public price |
| 6 | Which EFT channel? (GAP-012) | `eftprodongle.com` country tiles → detail pages; `fastprovision.com store EFT`; `"EFT" "halabtech" telegram`; `easy-unlocker.com halabtech` | Firecrawl | HalabTech found/not found on each EFT channel |
| 7 | Which UMT / FG / Avengers distributor? (GAP-013) | `fastunlocking.com UMT activation price`; `gsmeasyshop.com UMT`; `martview UMT 1 year`; ADY Unlocker FG credits price | Firecrawl, Parallel | Price/route match for ≥1 product line |
| 8 | Identities of IMEI "Source #2/#3" and "Server Direct" | `t.me/s/halabtech2?q=SOURCE+%232`; `"Source #3" MDM Tecno resellerpricing`; `"Clean IMEIs Server Direct" Mi Account JAPAN` | Firecrawl (Telegram), Exa | Any named source or narrowed to ≤2 candidates |
| 9 | Bulk public Service IDs (GAP-017) | Firecrawl with `waitFor`/actions on `/cart/group/<id>/viewmode/grid/service/product/?sortby=namea` | Firecrawl | ≥80 % of SKUs with pid |
| 10 | Long-tail vendor lists (GAP-018) | `"<tool> resellers" halabtech` for the 50 largest unchecked groups (see Service Groups where status = "Not checked"); schematic vendors ZXW, JCID, Refox, Orion, FCL, Zhizhen, YCS, Lanrui, W2R | Exa batch, Parallel | Top 50 checked |
| 11 | Catalog shrinkage 2022→2026 (GAP-021) | `web.archive.org/web/2023/https://server.halabtech.com/resellerpricing/server`; same for 2025; diff vs `data/catalog/server_catalog.json` | Firecrawl (Wayback) | List of dropped groups with dates; check if dropped lines map to a lost supplier |
| 12 | GSX "#225 / #33225" origin | `"33225" GSX`; `"Part Number (Mac/Watch)" "32596"`; servers with native service IDs in that range | Exa, Firecrawl search | Origin server identified or ruled out |

## Rules to keep
- Official reseller/distributor status ≠ direct API connection.
- Identical names / similar prices = leads only (most matches are HalabTech's own customers).
- Record every claim with URL, access date, ≤25-word excerpt, tool, confidence; append to the workbook, never delete prior rows.

## Ready-to-copy prompt

```
You are continuing the HalabTech supply-chain OSINT investigation (Rounds 1-6 done; verification date 2026-10-11).
1) Open HalabTech_Complete_Supply_Chain_Research.xlsx (17 sheets). Treat "Service Groups", "Supply Chain Relationships",
   "Evidence Register" (EV-001…EV-266), "Unknown Suppliers" and "Research Gaps" (GAP-001…022) as prior state.
   Read reports/HalabTech_Report_R4-R6_AR.md and data/findings/*.json. Append only; never delete rows.
2) Test Firecrawl, Parallel Search and Exa with one real call each; log every call (tool, input, ok) — never claim
   a tool you did not invoke. Firecrawl's shared limit is ~18 req/min: pace parallel agents accordingly.
3) Work the questions in reports/NEXT_RESEARCH_MISSION_R7.md in order (Chimera distributor; Code-GSM same-day price
   test; UnlocksPro direction; iRemove partner; cost×1.10 back-calculation; EFT channel; UMT/FG distributor;
   Source #2/#3 identity; pids; long-tail vendors; catalog shrinkage; GSX #225/#33225).
4) Evidence rules: vendor listing = authorised channel only; identical service names or prices = lead only;
   only a primary source naming the supply relationship can make it CONFIRMED. Use CONFIRMED / STRONG / LIKELY /
   UNKNOWN / DISPUTED.
5) Run a verification round: re-fetch every new STRONG/CONFIRMED claim with a different tool.
6) Deliver: updated workbook (new EV-267+, REL-106+, GAP-023+, CL-022+), Arabic report, updated Mermaid/PNG graph,
   progress table vs Round 6, ranked unresolved list, and the next mission file.
```
