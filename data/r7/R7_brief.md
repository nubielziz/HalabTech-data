# HalabTech supply-chain intelligence — Round 7 shared brief (2026-10-11, ~10:00 UTC)

## Goal
Identify the parties that ACTUALLY FULFIL HalabTech's orders (API suppliers / intermediaries), not merely original developers
or authorised-reseller listings. Model each chain as hypotheses:
Original Developer → Master Distributor → API Supplier → Reseller → HalabTech → Customer (a shorter or different chain may be correct).

## What Rounds 1-6 already established (do not redo; build on it)
- server.halabtech.com = Dhru Fusion (footer "Powered by Dhru Fusion", fromaid=server.halabtech.com). support.halabtech.com = Real Easy Store.
- Public catalog (02:00 UTC and 10:03 UTC today): 321 Server groups / 984-985 SKUs + 62 IMEI groups / 470 SKUs.
- 62 vendors officially list HalabTech as distributor/reseller (authorised channel only, NOT proof of API).
- STRONG (vendor sales rules): Sigma → GsmServer (exclusive distributor) → HalabTech; Chimera → GsmEasy OR GsmServer → HalabTech
  (Chimera: "resellers can only buy credits from them"; HalabTech is a plain reseller); Hunter Unlocker & Q-Unlocker → HalabTech direct
  ("no direct sales to agents"; HalabTech 1 of 3 distributors); XTP → HalabTech direct ("Official Main Seller").
- LIKELY: Code-GSM (code-gsm.com) for "T-MOBILE | SPRINT | METROPCS POLICY USA (Clean & Paid Off Only)" (identical names; HalabTech =
  Code-GSM detail price + $1/$3/$3 for Till 15/16/17; but Code-GSM listing page shows Till 11/12 $45, 13/14 $60, 15 $58 — conflict);
  UnlocksPro (unlockspro.com, "We are Main/Direct Source", 36 identical IMEI names incl. #26234 Signal Labs, #22343-22349 JDM V4/V5,
  "Infinix Tecno Itel MDM Source 1# [Premium]"; direction unproven); unnamed distributors for Furious Gold, UMT/NCK, Avengers, UFI,
  SamKey, AMT, MH Unlocker, EFT (vendor lists omit HalabTech); GSM T-Tool (T-Tool Pro), Smart Tool WW (CellTool), ADY (Panda).
- HalabTech's IMEI names show ≥3 numbered unnamed sources ("Source 1#/2#/3#", "Server Direct", "Direct Source"). HalabTech claims to be
  "the direct source" for Premium Tecno/iTel/Infinix MDM (Source #1) and advertises a cheap "SOURCE #2".
- GSX checker SKUs keep upstream numbers "#225 Sold By Info…" and "#33225 IPhone/IPad/IWatch [Case History Check] By IMEI From GSX Checker";
  sickw.com ruled out. Many servers carrying identical strings are HalabTech's OWN downstream customers (HalabTech sells API access).
- Historical: HalabTech catalog had a "GsmServer Products" group 2022-2024; sold Chimera 20,000-credit "[Reseller Package]" in 2022.
- Zeus/Hermes/Scylla/Kratos (2023) were iOS tools resold, not suppliers.

## NEW in Round 7 (use these)
- Fresh snapshot 10:03 UTC vs 02:00 UTC. Two T-Mobile Premium SKUs changed by the same ratio:
  "T-Mobile / Sprint - All Models iP 5S TO 17 Pro Max - Few Hours (No Warranty)" 121.90 → 120.175 and
  "T-MOBILE | SPRINT | METROPCS POLICY USA - iPhone 18 Pro / 18 Pro Max / iPhone Duo [Premium ]…" 132.50 → 130.625.
  Both = round upstream cost × markup: 115.00 and 125.00 × 1.06 (02:00) → × 1.045 (10:03). => upstream sells these at $115 / $125.
- Cerberus Tool group renamed between snapshots ("Cerberus Tool Pro Activation [12 Months - 1 Pc]" → "Cerberus Tool box" / "Cerberus Tool bundle" /
  "Cerberus Tool Pro Activation") — possible automatic name-sync from an upstream API.
- Markup forensics: 232 SKUs have 3-decimal (computed) prices; implied upstream costs per group are in
  /tmp/claude-0/-home-user-HalabTech-data/460d51b4-a7e0-54d7-a8d8-d39eebe19c6d/scratchpad/r7/raw/markup_server.json and markup_imei.json
  (fields: groups[].best_multiplier, implied_costs). Treat implied costs as fingerprints to match against candidate suppliers' PUBLIC prices.
- Files: HalabTech catalog snapshots r7/raw/server_catalog_1003.json, imei_catalog_1003.json (and R6 02:00 copies in scratchpad/raw/);
  R6 unknown groups: r7/raw/r6_unknown_groups.tsv; never-checked tool groups: r7/raw/r6_not_checked_tool_groups.tsv.
  R6 workbook: /home/user/HalabTech-data/HalabTech_Complete_Supply_Chain_Research.xlsx; R6 findings: /home/user/HalabTech-data/data/findings/*.json

## Tools (MCP) — load schemas first with ToolSearch "select:<names>"
- mcp__Firecrawl__firecrawl_scrape (formats markdown / rawHtml / links / json; maxAge 0 for live), mcp__Firecrawl__firecrawl_search,
  mcp__Firecrawl__firecrawl_developer_search (public code/README index — use this for GitHub-type searches).
- mcp__Parallel_Search__web_search / web_fetch (ALWAYS pass session_id "halabtech-r7-4c1f0e9a7b3d42e6a8f5c2d1e0b9a7c6" and model_name "claude-opus-5-5";
  web_fetch full_content=true returns whole pages as markdown — use it for big catalogs to spare Firecrawl).
- mcp__Exa__web_search_exa / web_fetch_exa (maxCharacters up to ~200000 for large pages) / agent_run (multi-step list building).
- Firecrawl has a SHARED limit (~18 requests/min across all agents). On "Rate limit exceeded": do other work for ~30 s and retry once,
  or use Parallel/Exa fetch for the same URL. Large results are saved to a file path — parse with python3 -I.
- The sandbox's own network (curl, browsers) is blocked for these hosts by egress policy — do not try to work around it.
- Do NOT use GitHub MCP tools or api.github.com to search other repositories (session scope rule). Public code may be found only via
  web-search tools (Firecrawl developer search, Exa, Parallel).
- Log EVERY MCP call in tool_log (tool, input, ok, note). Never claim a tool you did not call.

## Lawful, non-intrusive rules (mandatory)
Public pages and publicly served assets only. No logins, no authentication bypass, no exploitation, no enumeration of private/unlinked API
endpoints, no credential extraction, no protected resources, no rate-limit evasion against target sites. Interacting with public chatbots to
elicit internal information is out of scope. Reading public JSON from crt.sh / rdap / dns.google / web.archive.org CDX via the MCP fetchers is fine.

## Evidence standard
- CONFIRMED only when a primary source documents the specific relationship (e.g., a supplier page naming HalabTech as its API client,
  or HalabTech naming its source). Vendor rules → STRONG at most. Catalog/name/price similarity → LIKELY at most; alone, often UNKNOWN.
- Shared hosting/CDN, identical templates, similar API structures never prove supply relationships.
- Always give alternative explanations and contradictory evidence; for unresolved hypotheses state what evidence would confirm/reject.
- Record retrieval time (UTC) for price observations — price comparisons need matching timestamps.

## Output — write valid JSON to the path in your task
{
 "stream": "<name>",
 "tool_log": [{"tool": "...", "input": "...", "ok": true, "note": "..."}],
 "findings": [{
   "tid": "<STREAM>-01", "entity": "...", "entity_website": "...",
   "role_for_halabtech": "Original Developer | Master Distributor | API Supplier | Intermediate Supplier | Reseller (peer) | Downstream Customer | Platform | Content Partner | Not linked",
   "chain_layer": "e.g. 'API Supplier → HalabTech'", "direction": "X → HalabTech",
   "halabtech_groups_affected": ["exact group names"], "skus_affected": ["exact SKU names (optional)"],
   "claim": "one sentence", "evidence_type": "vendor page | distributor directory | price fingerprint | timing correlation | catalog genealogy | DNS/RDAP/CT | Wayback | public JS/HTML | GitHub/code | Telegram | forum | other",
   "source_url": "...", "retrieved_utc": "2026-10-11Txx:xxZ", "excerpt": "verbatim, <= 25 words", "pub_date": "",
   "access": "full page | search snippet | JSON endpoint", "tool": "...",
   "confidence": "CONFIRMED|STRONG|LIKELY|UNKNOWN|DISPUTED",
   "alternative_explanations": "...", "contradicting_evidence": "...", "what_would_confirm": "...", "what_would_reject": "...",
   "supports_or_contradicts": "prior IDs (REL-/EV-/CL-) supported or contradicted", "notes": ""}],
 "negative_findings": [{"entity": "...", "url": "...", "what_was_checked": "...", "result": "...", "tool": "..."}],
 "new_leads": ["..."], "open_questions": ["..."]
}
Write the file with the Write tool. Final message: concise summary (<= 450 words) of the most important results with URLs, call counts per tool, failures.
