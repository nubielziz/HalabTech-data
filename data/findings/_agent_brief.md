# HalabTech supply-chain OSINT — shared brief for research agents (Round 4–5, date 2026-10-11)

## Context
HalabTech (server.halabtech.com = Dhru Fusion wholesale GSM server, confirmed by "Powered by Dhru Fusion" footer;
support.halabtech.com = firmware portal on Real Easy Store; also store./tools./news./point.halabtech.com) is a
wholesale aggregator of GSM tool activations/credits, IMEI unlocks, iCloud/FRP/MDM/Mi-Account services, gift cards, etc.
Contacts: telegram @htsupport, t.me/halabtech2, WhatsApp +963992951910 / +90507058173, info@halabtech.com, halabtech.cert@gmail.com.

The live public catalog (scraped today with Firecrawl) has 321 "server" groups / 985 services and 62 "IMEI" groups / 470 services.
Lists are in:
- /tmp/claude-0/-home-user-HalabTech-data/460d51b4-a7e0-54d7-a8d8-d39eebe19c6d/scratchpad/raw/server_groups.txt
- /tmp/claude-0/-home-user-HalabTech-data/460d51b4-a7e0-54d7-a8d8-d39eebe19c6d/scratchpad/raw/server_list.txt  (group | service | delivery | price)
- /tmp/claude-0/-home-user-HalabTech-data/460d51b4-a7e0-54d7-a8d8-d39eebe19c6d/scratchpad/raw/imei_list.txt

## Already established in Rounds 1–3 (do NOT redo unless verifying a contradiction)
Vendors that list HalabTech as distributor/reseller on their own sites: DFT Pro (dftpro.com/dealers), ChimeraTool (chimeratool.com/en/resellers),
Octoplus (octoplusbox.com/buynow), Xiaomi King Tool, E-GSM (egsmtool.com "Distributer" vs egsmkey.com "Reseller"), Deep Unlocker,
UnlockTool (reseller, "PAKISTAN - WORLDWIDE"), MDMFix, General Unlocker, TFM Tool, AuthFlash.
Found in a Round-4 smoke test (need full verification): Cheetah Tool (cheetah-tool.com/resellers), HW-Key (hwkey.com/resellers),
EMT (emegsm.com/en/reseller.asp), DeviceSavior (devicesavior.com/en/reseller), SK Unlocker (s-k-unlocer.com/distributors.html),
OumseGsm (oumsegsm.com/resellers).
GsmServer resells HalabTech products since 14.10.2022 and is on HalabTech's "World Agents" list; no evidence yet that GsmServer supplies HalabTech.
HalabTech supplies firmware content to ChimeraTool ("HalabTech Add-On"). ChimeraTool doc reportedly says resellers can only buy credits from
two distributors (GsmEasy, GsmServer) — only seen as a search snippet so far.
EFT Dongle distributor list (eft-dongle.easy-firmware.com/distributor-reseller): SimSim Electronics (Dubai), GsmServer (HK), KhaledGsm (Algeria), Yemen contact — HalabTech not seen.
ZERO direct API suppliers have been identified. That is the main goal now.

## Tools — you MUST use these MCP tools (load schemas first with ToolSearch "select:<names>")
- mcp__Firecrawl__firecrawl_scrape (url, formats ["markdown"], onlyMainContent true; maxAge 0 for live). mcp__Firecrawl__firecrawl_search also exists.
  Large results get saved to a file path — parse it with python3 -I (JSON with a "markdown" key).
- mcp__Parallel_Search__web_search (objective + search_queries list) and mcp__Parallel_Search__web_fetch (urls + objective).
  ALWAYS pass session_id "halabtech-r4-7f3c9a21b5e84d0c9e1a2b3c4d5e6f70" and model_name "claude-opus-5-5".
- mcp__Exa__web_search_exa (query + objective + numResults) and mcp__Exa__web_fetch_exa (urls, maxCharacters).
Plain curl from the sandbox is blocked by the proxy for these sites — do not rely on it.
Log EVERY MCP call you make (tool, query/url, ok/failed, short note) in tool_log. Never claim a tool was used unless you called it.
Budget: roughly 25–45 MCP calls. Prefer batching queries. Stop early if a lead is exhausted.

## Rules of evidence
- Public pages only. No logins, no bypassing auth, no private supplier configs.
- Keep these roles distinct: Original Vendor; Official Distributor (vendor-listed); Official Reseller (vendor-listed);
  Direct API Supplier (the party that actually fulfils HalabTech orders); Intermediate Supplier (sits between vendor and HalabTech);
  Downstream Reseller (buys from HalabTech); Peer; Platform; Content Partner.
- A vendor listing HalabTech as distributor/reseller proves an authorised sales channel, NOT a direct API link.
  It does, however, make "HalabTech buys direct from vendor" LIKELY for vendors whose model is vendor→distributor.
- A vendor that states it sells ONLY through named distributors is strong evidence for an intermediate supplier.
- Identical service names or similar prices across Dhru servers are leads, NOT proof. Note them as LIKELY at most unless corroborated.
- Confidence labels: CONFIRMED / STRONG / LIKELY / UNKNOWN / DISPUTED.
- Record negative findings too (e.g., "HalabTech absent from X's full reseller list", with URL and access type).

## Output — write a JSON file (path given in your task) with this shape
{
 "stream": "<name>",
 "tool_log": [{"tool": "...", "input": "...", "ok": true, "note": "..."}],
 "findings": [{
   "tid": "<STREAM>-01", "entity": "...", "entity_website": "...",
   "role_for_halabtech": "<one of the roles above, or 'Not listed'>",
   "direction": "e.g. 'Hydra -> HalabTech' or 'HalabTech -> X'",
   "halabtech_groups_affected": ["exact group names from the catalog lists"],
   "claim": "one sentence",
   "source_url": "...", "source_type": "Vendor official | Distributor | Reseller store | Forum | Social | HalabTech official | Archive | Other",
   "excerpt": "verbatim, <= 25 words", "pub_date": "", "access": "full page | search snippet",
   "tool": "which MCP tool produced it", "confidence": "CONFIRMED|STRONG|LIKELY|UNKNOWN|DISPUTED",
   "supports_or_contradicts": "what prior conclusion it supports/contradicts", "notes": ""}],
 "negative_findings": [{"entity": "...", "url": "...", "what_was_checked": "...", "result": "...", "tool": "..."}],
 "new_leads": ["..."],
 "open_questions": ["..."]
}
Write the file with the Write tool (valid JSON). Your final message: a concise summary (<= 500 words) of the most important
findings with URLs, plus counts of calls per MCP tool and any tool failures.
