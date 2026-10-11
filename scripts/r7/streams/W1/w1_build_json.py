"""Build W1.json from the partial tool log + remaining tool entries + findings. Usage: python3 -I w1_build_json.py <raw_dir> <out_json>"""
import json, sys

raw_dir, out = sys.argv[1], sys.argv[2]
tool_log = json.load(open(raw_dir + '/tool_log_partial.json'))
tool_log += [
    {"tool": "mcp__Parallel_Search__web_fetch", "input": "support sitemap core, halabtech.com page-sitemap, Wayback 2023 server sitemap (retry)", "ok": False, "note": "Too Many Requests (2nd 429)"},
    {"tool": "mcp__Firecrawl__firecrawl_scrape", "input": "https://web.archive.org/web/20200602063355/https://server.halabtech.com/server/productsandservices.html markdown", "ok": True, "note": "2020-06-02 capture, 40 server groups incl. 'GsmServer Products', 'APPLE ID INFO' (_source 2/#S1/#S3/*Supplier 3*), 'API Test', 'Infinity online services2' (AUTO API); extract saved wb_20200602_server_productsandservices_extract.md"},
    {"tool": "mcp__Firecrawl__firecrawl_scrape", "input": "https://web.archive.org/web/20200531081236/https://server.halabtech.com/imei/productsandservices.html markdown onlyMainContent", "ok": True, "note": "55 IMEI groups; SOURCE A/B, #S1-#S4, Server 2#, Source 2, '1250# iP Gsx Check', 'From Gsx Checker'; saved wb_20200531_imei_productsandservices.md"},
    {"tool": "mcp__Parallel_Search__web_fetch", "input": "support sitemap core + halabtech.com page-sitemap (2 URLs)", "ok": False, "note": "Too Many Requests (3rd 429)"},
    {"tool": "mcp__Exa__web_fetch_exa", "input": "support sitemap core + halabtech.com page-sitemap.xml", "ok": False, "note": "CRAWL_UNEXPECTED_CONTENT_TYPE (XML)"},
    {"tool": "mcp__Firecrawl__firecrawl_scrape", "input": "https://support.halabtech.com/index.php?a=sitemap&sec=core rawHtml", "ok": True, "note": "7 core URLs only"},
    {"tool": "mcp__Firecrawl__firecrawl_scrape", "input": "https://halabtech.com/page-sitemap.xml rawHtml", "ok": True, "note": "14 page URLs (Yoast); no supplier/partner pages"},
]

F = []
def f(**kw):
    base = {"tid": "", "entity": "", "entity_website": "", "role_for_halabtech": "", "chain_layer": "", "direction": "",
            "halabtech_groups_affected": [], "skus_affected": [], "claim": "", "evidence_type": "", "source_url": "",
            "retrieved_utc": "", "excerpt": "", "pub_date": "", "access": "full page", "tool": "", "confidence": "",
            "alternative_explanations": "", "contradicting_evidence": "", "what_would_confirm": "", "what_would_reject": "",
            "supports_or_contradicts": "", "notes": ""}
    base.update(kw)
    F.append(base)

f(tid="W1-01", entity="Cloudflare (DNS/CDN/email routing) + GoDaddy (registrar)", entity_website="https://www.cloudflare.com",
  role_for_halabtech="Platform", chain_layer="Infrastructure (not in supply chain)", direction="Cloudflare -> HalabTech (hosting edge)",
  claim="halabtech.com (GoDaddy, registered 2015-01-16) uses Cloudflare NS anirban/galilea; all checked HalabTech hosts resolve to the same Cloudflare edge IPs and mail goes through Cloudflare Email Routing.",
  evidence_type="DNS/RDAP/CT", source_url="https://rdap.org/domain/halabtech.com ; https://dns.google/resolve?name=halabtech.com&type=NS",
  retrieved_utc="2026-10-11T10:16Z", excerpt="\"eventAction\":\"registration\",\"eventDate\":\"2015-01-16T21:53:30Z\" ... ANIRBAN.NS.CLOUDFLARE.COM ... GALILEA.NS.CLOUDFLARE.COM",
  access="JSON endpoint", tool="mcp__Firecrawl__firecrawl_scrape (RDAP); mcp__Parallel_Search__web_fetch (dns.google)", confidence="CONFIRMED",
  alternative_explanations="n/a (infrastructure fact). Shared Cloudflare edge IPs are used by millions of sites and prove nothing about suppliers.",
  contradicting_evidence="none", what_would_confirm="already confirmed by RDAP + DNS", what_would_reject="n/a",
  supports_or_contradicts="Context for OWN-01 (Dhru platform)",
  notes="A records (TTL 300) for halabtech.com, server., support., news., store., tools., chat., techub.: 104.26.0.72 / 104.26.1.72 / 172.67.70.118. MX: route1/2/3.mx.cloudflare.net. DMARC p=none rua=info@halabtech.com. TXT: 3 google-site-verification tokens + detectify-verification (security-scanner ownership proof). RDAP last changed 2026-07-21; expires 2029-01-16; DNSSEC unsigned. Earlier third-party snapshot (getstat) showed old NS nikon/romina.ns.cloudflare.com.")

f(tid="W1-02", entity="Layout Team (layouteam.com) - Arabic software/cloud/web-design firm", entity_website="https://layouteam.com",
  role_for_halabtech="Platform", chain_layer="Hosting/mail provider (not in supply chain)", direction="Layout Team -> HalabTech (hosting)",
  claim="HalabTech's SPF authorises Layout Team's server (176.9.147.187 = host.layouteam.com) and include:layouteam.com; api.store.halabtech.com resolves directly to that server, and layouteam.com's own SPF also lists 95.216.33.175, the IP in server.halabtech.com's SPF.",
  evidence_type="DNS/RDAP/CT", source_url="https://dns.google/resolve?name=halabtech.com&type=TXT ; https://dns.google/resolve?name=layouteam.com&type=TXT ; https://dns.google/resolve?name=187.147.9.176.in-addr.arpa&type=PTR",
  retrieved_utc="2026-10-11T10:16Z", excerpt="v=spf1 ip4:176.9.147.187 include:layouteam.com include:_spf.mx.cloudflare.net ~all",
  access="JSON endpoint", tool="mcp__Parallel_Search__web_fetch (dns.google)", confidence="CONFIRMED",
  alternative_explanations="Layout Team may simply be HalabTech's web/hosting contractor (reseller hosting on Hetzner); it does not imply any role in fulfilling GSM orders.",
  contradicting_evidence="none",
  what_would_confirm="Layout Team portfolio page naming HalabTech; same SPF/PTR pattern persisting over time",
  what_would_reject="SPF entries removed / shown to belong to a different operator",
  supports_or_contradicts="New (no prior ID); context for OWN-01",
  notes="server.halabtech.com TXT = 'v=spf1 +mx +a +ip4:95.216.33.175 ~all' (PTR 95-216-33-175.ptr, Hetzner range); layouteam.com TXT = 'v=spf1 ip4:176.9.147.187 ip4:95.216.33.175 +mx +a ~all'. Implication (LIKELY, not verified): the Dhru Fusion instance is self-hosted on a Layout-Team-managed Hetzner server rather than on Dhru's cloud. CT shows cPanel AutoSSL sets for tools.* and store.* (shared-hosting pattern). Origin IPs were NOT probed (non-intrusive rule).")

f(tid="W1-03", entity="HTD / HTD CRM SaaS (htdtech.dev)", entity_website="https://htdtech.dev/",
  role_for_halabtech="Platform", chain_layer="Store software (Platform) -> HalabTech store; possibly HalabTech-affiliated",
  direction="HTD -> HalabTech (store platform); HalabTech also resells HTD stores",
  halabtech_groups_affected=["store.halabtech.com: HTD Build Your Store (3 services)", "store.halabtech.com: Activation | Credits Tools (82 services)"],
  claim="store.halabtech.com runs on the HTD CRM SaaS (footer '(c) 2026 HTD' -> htdtech.dev), whose FAQ says stores integrate 'DHRU or HTD Scripts APIs'; HalabTech's store sells 'HTD Build Your Store' plans.",
  evidence_type="public JS/HTML", source_url="https://store.halabtech.com/ ; https://htdtech.dev/",
  retrieved_utc="2026-10-11T10:17Z", excerpt="Which API service providers can I integrate with? Our platform supports integration with DHRU or HTD Scripts APIs.",
  access="full page", tool="mcp__Firecrawl__firecrawl_scrape (store); mcp__Parallel_Search__web_fetch (htdtech.dev)", confidence="CONFIRMED",
  alternative_explanations="HTD may be an independent Turkish/Syrian developer whose store HalabTech merely resells; 'HTD' could also stand for HalabTech Development (an icon images/icon/htd.jpg existed on server.halabtech.com per Wayback) - ownership unproven.",
  contradicting_evidence="none",
  what_would_confirm="HTD site or Telegram (t.me/HTDtechdev) naming HalabTech as owner/partner; store products showing Dhru API sync from server.halabtech.com",
  what_would_reject="HTD client list showing it is an unrelated vendor with many unrelated GSM clients",
  supports_or_contradicts="New",
  notes="Store: Laravel + Livewire + Metronic theme; images/favicon from api.store.halabtech.com (176.9.147.187, Layout Team server); Telegram bot telegram.me/storehalabtechbot; categories Games|Gift Cards (16), Activation|Credits Tools (82), IMEI Services (8), Mobile Recharge (5), Voucher Cards Server Halabtech (1), Ready Account (0), HTD Build Your Store (3). Store app JS (app-D2jpX1vH.js) is only an axios 1.6.8 bundle - no API endpoints. HTD contact is a Turkish (+90) WhatsApp number; pricing Bronze $289 / Gold $799 / Platinum $1199 per year. Exa search found no other HTD-built GSM store.")

f(tid="W1-04", entity="HalabTech AI chat (in-house n8n webhook chat.halabtech.com; RAG API techub.halabtech.com/halabtech-rag)", entity_website="https://server.halabtech.com/AiBot/chat-widget.html",
  role_for_halabtech="Not linked", chain_layer="Customer-support tooling (first-party)", direction="n/a",
  claim="The 'HalabTech AI' widgets on server./support. post only to https://chat.halabtech.com (an n8n webhook per code comments) and halabtech.com's WordPress plugin uses https://techub.halabtech.com/halabtech-rag; no third-party chat, AI or supplier endpoint is referenced.",
  evidence_type="public JS/HTML", source_url="https://server.halabtech.com/AiBot/chat-widget.html ; https://server.halabtech.com/ ; https://support.halabtech.com/ ; https://halabtech.com/",
  retrieved_utc="2026-10-11T10:16Z", excerpt="Header Auth Key (must match n8n credential)",
  access="full page", tool="mcp__Firecrawl__firecrawl_scrape", confidence="CONFIRMED",
  alternative_explanations="The n8n workflow behind chat.halabtech.com may call external LLM or order APIs server-side; that is invisible from public JS and was not probed (no chat messages sent).",
  contradicting_evidence="none",
  what_would_confirm="n/a (front-end fact)", what_would_reject="n/a",
  supports_or_contradicts="New",
  notes="Widget payload = {message, session_id, timestamp}; quick-reply topics include payment methods, order delay, missing files, technical issues. A static client-side X-Api-Key header value is embedded in the public HTML; its value was deliberately NOT recorded or used (redacted in raw captures). halabtech.com config exposes a per-visitor guest token (redacted) with header X-HalabTech-Widget-Token and tier 'guest' (paid members only). CT also shows aireply.halabtech.com (2026-09-18) and agent.halabtech.com (2026-09-30) - likely further AI endpoints.")

f(tid="W1-05", entity="Analytics / ad identifiers (Google Analytics 4, Google AdSense, Cloudflare Web Analytics)", entity_website="",
  role_for_halabtech="Not linked", chain_layer="n/a", direction="n/a",
  claim="HalabTech properties carry GA4 G-3FW622FWW6 (support., halabtech.com), AdSense publisher ca-pub-9647107642564560 (support., news., halabtech.com) and one Cloudflare beacon token on every property; no GTM, Facebook pixel, Yandex, Clarity, Tawk or Crisp IDs were found, and web searches for the IDs found no other domains.",
  evidence_type="public JS/HTML", source_url="https://support.halabtech.com/ ; https://halabtech.com/ ; https://news.halabtech.com/",
  retrieved_utc="2026-10-11T10:11Z", excerpt="gtag('config', 'G-3FW622FWW6');",
  access="full page", tool="mcp__Firecrawl__firecrawl_scrape; mcp__Parallel_Search__web_search (ID pivot)", confidence="CONFIRMED",
  alternative_explanations="Search engines rarely index tracking IDs, so 'no other domain found' is weak negative evidence.",
  contradicting_evidence="none",
  what_would_confirm="a reverse-analytics service (e.g. publicwww/BuiltWith) listing other sites with ca-pub-9647107642564560 or G-3FW622FWW6",
  what_would_reject="n/a",
  supports_or_contradicts="New",
  notes="Cloudflare Web Analytics beacon token 2e33eec1cd624bd0adcc9d36a06229c5 identical on server., support., news., store., tools., halabtech.com and the AiBot widget -> one Cloudflare account. robots.txt on support./halabtech.com explicitly Allow Mediapartners-Google (AdSense). server.halabtech.com (Dhru) carries no analytics/pixel at all.")

f(tid="W1-06", entity="SosoGSM (sosogsm.net / sosogsm.ro) - GSM unlock server", entity_website="https://sosogsm.net",
  role_for_halabtech="Downstream Customer", chain_layer="HalabTech -> SosoGSM (inferred AI-chat deployment; supply role unknown)",
  direction="HalabTech -> SosoGSM (inferred)",
  claim="Certificate Transparency shows HalabTech created chatsosogsm.halabtech.com and chatsosogsm2.halabtech.com (certs issued 2026-08-29), indicating HalabTech hosts chat endpoints for SosoGSM, another GSM unlock server.",
  evidence_type="DNS/RDAP/CT", source_url="https://api.certspotter.com/v1/issuances?domain=halabtech.com&include_subdomains=true&expand=dns_names&expand=issuer",
  retrieved_utc="2026-10-11T10:13Z", excerpt="\"dns_names\": [ \"chatsosogsm.halabtech.com\", \"halabtech.com\" ] ... \"not_before\": \"2026-08-29T12:33:44Z\"",
  access="JSON endpoint", tool="mcp__Parallel_Search__web_fetch", confidence="LIKELY",
  alternative_explanations="'sosogsm' could be an unrelated label (test instance) or SosoGSM could be a supplier/partner given chat access; naming alone shows a relationship, not its direction or any order flow.",
  contradicting_evidence="none",
  what_would_confirm="SosoGSM site embedding a widget that posts to chatsosogsm.halabtech.com; SosoGSM catalog mirroring HalabTech SKU names (downstream) or vice versa",
  what_would_reject="the subdomain serving a different, non-SosoGSM project",
  supports_or_contradicts="New; consistent with OWN-08/OWN-09 pattern (other servers reselling HalabTech)",
  notes="SosoGSM: 'SosoGsmUnlock Server' forum at support.sosogsm.net; sosogsm.net registered 2016-11-12 (Key-Systems) per third-party snapshot. A similar subdomain chatmenet.halabtech.com (certs 2026-09-03) suggests a second client ('menet', unidentified).")

f(tid="W1-07", entity="GsmServer (gsmserver.com)", entity_website="https://gsmserver.com",
  role_for_halabtech="Intermediate Supplier", chain_layer="Sigma / Octoplus / Boot-Loader / GB Key developers -> GsmServer -> HalabTech (historical, 2020; Smart Clip was a separate group then)",
  direction="GsmServer -> HalabTech",
  halabtech_groups_affected=["GsmServer Products (2020-06-02 archived catalog; absent today)"],
  skus_affected=["Sigma Pack 1 Activation Code", "Sigma Pack 2 Activation", "Sigma Pack 3 Activation Code", "Sigma Pack 4 Activation", "SigmaKey Huawei Edition Upgrade to SigmaKey with Pack 1, 2, 3,4", "Octoplus / Octopus Box Credits For Existing Users (Instant)", "Octoplus Full Digital License 1 Year", "Boot Loader v2.0 Activation", "GB Key Act1"],
  claim="The archived 2020-06-02 server catalog already had a 'GsmServer Products' group of 26 SKUs (Sigma Packs 1-4, SigmaKey Huawei upgrade, Octoplus credits and digital licences, Boot-Loader 2.0, GB Key), extending HalabTech's own GsmServer source label back to mid-2020.",
  evidence_type="Wayback", source_url="https://web.archive.org/web/20200602214537/https://server.halabtech.com/server/productsandservices.html",
  retrieved_utc="2026-10-11T10:21Z", excerpt="GsmServer Products | Delivery Time | Price ... Sigma Pack 1 Activation Code | 0 Instant | $63",
  pub_date="2020-06-02", access="full page", tool="mcp__Firecrawl__firecrawl_scrape", confidence="CONFIRMED",
  alternative_explanations="The label could mean 'products GsmServer distributes' (catalog copied from GsmServer) rather than an automated API link; either way GsmServer is named as the 2020 source. It says nothing about who supplies Sigma/Octoplus today.",
  contradicting_evidence="Octoplus lists HalabTech as an official reseller (A1-10), which could allow direct purchase from Octoplus.",
  what_would_confirm="GsmServer reseller/API documentation or invoices; current HalabTech Sigma/Octoplus prices matching GsmServer reseller prices with a fixed markup",
  what_would_reject="evidence that the group label was a brand name unrelated to GsmServer the distributor",
  supports_or_contradicts="Supports C-07, V-10 (extends 2022-2024 dating to 2020-06) and A1-08 (Sigma via exclusive distributor GsmServer); adds Octoplus to the GsmServer-labelled items.",
  notes="Same capture: 'Chemira Tool' group (Chimera Tool Credits $0.12; PRO $133.09; Samsung $78.81) - no source named. Capture footer already shows 'Powered by Dhru Fusion'. Contact in 2020: WhatsApp +905070585173 (Turkey).")

f(tid="W1-08", entity="Unnamed numbered upstream sources (Source A/B, S1-S4, Source 2, Supplier 3, Server #1/#2/#3, 'Gsx Checker')", entity_website="",
  role_for_halabtech="API Supplier", chain_layer="unnamed API sources -> HalabTech (since at least 2020)", direction="unnamed -> HalabTech",
  halabtech_groups_affected=["APPLE ID INFO (2020)", "Device info CHeckers (2020)", "gsx check (2020)", "UK Vodafone (2020)", "Free Fire Server #2 (2020)", "Pubg Server #3 (2020)", "Pubg Mobile Server #1 (2020)", "Infinity online services2 (2020)", "API Test / API test (2020)"],
  skus_affected=["UK Vodafone iPhone X (100% Success ) Slow SERVICE { SOURCE B }", "Apple ID - USA T-Mobile Only (Owner Info) By IMEI Only *Supplier 3 *", "Carrier + SIM Lock Status #S4 (with Blacklist History )", "1250# iP Gsx Check (Carrier + Simlock Status) By SN [No Refund For Invalid SN] [1-48 Hours]", "Iphone Sold By + Case Check + Replacement Check By IMEI From Gsx Checker", "SPT-Box software activation for Infinity [BEST]"],
  claim="Archived May/June 2020 catalogs already label at least four anonymous IMEI sources (Source A/B, #S1-#S4, 'Source 2', '*Supplier 3*'), numbered game servers, an 'API Test' group and 'AUTO API' delivery strings, and use the upstream-style '1250#' prefix and 'From Gsx Checker' wording that persists in 2026.",
  evidence_type="Wayback", source_url="https://web.archive.org/web/20200531081236/https://server.halabtech.com/imei/productsandservices.html ; https://web.archive.org/web/20200602214537/https://server.halabtech.com/server/productsandservices.html",
  retrieved_utc="2026-10-11T10:22Z", excerpt="UK Vodafone iPhone X (100% Success ) Slow SERVICE { SOURCE B }",
  pub_date="2020-05-31 / 2020-06-02", access="full page", tool="mcp__Firecrawl__firecrawl_scrape", confidence="CONFIRMED",
  alternative_explanations="Numbered labels prove multiple fulfilment routes, not their identity; 'AUTO API' text may be a delivery-time field copied from an upstream catalog.",
  contradicting_evidence="none",
  what_would_confirm="matching 2020 archived catalogs of candidate suppliers with the same '1250#' numbering and 'From Gsx Checker' wording",
  what_would_reject="evidence the labels were invented internally with no upstream counterpart",
  supports_or_contradicts="Supports OWN-03 (numbered unnamed sources) and OWN-04 (#225/#33225 'From GSX Checker' upstream artifacts) and shows the practice dates to 2020.",
  notes="2020 server catalog had 40 groups; 2020 IMEI catalog 55 groups. 'Infinity online services2' and 'Micro Box Activations 2' are duplicate groups suggesting a second source for Infinity/Micro-Box products. 'Iphone Sold By + Case Check + Replacement Check By IMEI From Gsx Checker' (2020) ~ today's '#33225 IPhone/IPad/IWatch [Case History Check] By IMEI From GSX Checker'.")

f(tid="W1-09", entity="HalabTech (self-description, DISTRIBUTOR page 2022)", entity_website="https://server.halabtech.com/pages/DISTRIBUTOR",
  role_for_halabtech="Reseller (peer)", chain_layer="API suppliers -> HalabTech -> 'Web Owner' sub-servers", direction="upstream API -> HalabTech -> downstream servers",
  claim="In July 2022 HalabTech stated that most of its services are fulfilled automatically via API and offered a 'Web Owner' package (minimum $3,000 top-up) for other server owners, besides Reseller ($600) and Big Reseller ($1,250).",
  evidence_type="Wayback", source_url="https://web.archive.org/web/20220705073059/https://server.halabtech.com/pages/DISTRIBUTOR",
  retrieved_utc="2026-10-11T10:17Z", excerpt="Most of our services using API that's mean it is auto complete.",
  pub_date="2022-07-05", access="full page", tool="mcp__Parallel_Search__web_fetch", confidence="CONFIRMED",
  alternative_explanations="'API' may include HalabTech's own automation (in-house remote services) as well as upstream suppliers.",
  contradicting_evidence="OWN-05 shows some groups are fulfilled in-house (remote box sharing, hardware).",
  what_would_confirm="n/a (self-statement)", what_would_reject="n/a",
  supports_or_contradicts="Supports OWN-03 and the 'HalabTech sells API access' note in the brief (downstream servers carrying identical strings).",
  notes="Current home page slider says 'We're GSM Tools Distributor: contact us for the best prices'. Wayback CDX also shows /pages/autoPayment (2022), /pages/usdt, /pages/verifyId, /pages/VisaPayment (2024), /pages/samsungPatch and /pages/Offer (2023), and an archived icon /images/icon/apiTest.jpg (2022-09).")

f(tid="W1-10", entity="HalabTech (home page recruitment banner)", entity_website="https://server.halabtech.com/",
  role_for_halabtech="Reseller (peer)", chain_layer="Original Developers / sources -> HalabTech (direct deals sought)", direction="sources/tool owners -> HalabTech",
  claim="The live server.halabtech.com header slider invites upstream sources and tool owners to contact HalabTech for deals, alongside 'We're GSM Tools Distributor'.",
  evidence_type="public JS/HTML", source_url="https://server.halabtech.com/",
  retrieved_utc="2026-10-11T10:08Z", excerpt="If you're Source or Tool owner, contact us for a deal",
  access="full page", tool="mcp__Firecrawl__firecrawl_scrape", confidence="CONFIRMED",
  alternative_explanations="Marketing text; shows intent to buy direct, not which deals exist.",
  contradicting_evidence="none", what_would_confirm="n/a", what_would_reject="n/a",
  supports_or_contradicts="Consistent with direct-from-developer relationships (Hunter Unlocker, Q-Unlocker, XTP) and with numbered 'Source' labels (OWN-03).",
  notes="Same slider row 2: 'have Solution / Files To Upload By Your Name?' (WhatsApp +963992951910). Link to t.me/htsupport for the deal.")

f(tid="W1-11", entity="Platform history of server.halabtech.com (RoyalPanel-era panel 2019 -> Dhru Fusion by 2020-06)", entity_website="https://server.halabtech.com/",
  role_for_halabtech="Platform", chain_layer="n/a (platform genealogy)", direction="n/a",
  claim="Wayback shows a different unlock panel in May-June 2019 (admin path /RoyalPanel/ incl. refreshapiorders.php; front-end /unlock/ with stock 'Direct Wholesale Supplier' copy), Dhru Fusion's productsandservices.html URLs by 2020-05/06, and Dhru's current URL scheme from 2020-10-26.",
  evidence_type="Wayback", source_url="https://web.archive.org/web/20190525050718/http://server.halabtech.com:80/unlock ; https://web.archive.org/cdx/search/cdx?url=server.halabtech.com/*&output=json&fl=timestamp,original,statuscode&collapse=urlkey&limit=2000",
  retrieved_utc="2026-10-11T10:17Z", excerpt="#1 Direct Wholesale Supplier For iCloud Clean All Major Networks!",
  pub_date="2019-05-25", access="full page", tool="mcp__Parallel_Search__web_fetch", confidence="CONFIRMED",
  alternative_explanations="The 2019 'Direct Wholesale Supplier' line is template boilerplate common to unlock-panel themes and is not evidence of HalabTech being a source.",
  contradicting_evidence="none", what_would_confirm="n/a", what_would_reject="n/a",
  supports_or_contradicts="Extends OWN-01 (Dhru) backwards; C-17 catalog history",
  notes="CDX: 717 unique server URLs 2019-2026; 2019-05-17 root = 'We'll be back soon! ... HALABTECH-TEAM' maintenance page. /RoyalPanel/ paths (dashboard.php, smsgateways.php, refreshapiorders.php, onlinecustomers.php) are admin pages - only CDX metadata was read, nothing beyond public archive index. Archived 2019 link 'www.gsmtool.net' (404 relative link).")

f(tid="W1-12", entity="Tool-developer sites named inside HalabTech SKU names (22 domains)", entity_website="",
  role_for_halabtech="Original Developer", chain_layer="Original Developer -> (direct reseller panel or unknown intermediary) -> HalabTech", direction="developer -> HalabTech (path unknown)",
  halabtech_groups_affected=["Anonymous Tool", "Repair-Fix Xiaomi Auth Tool", "RADEX FRP TOOL", "tool.emmc-ufs", "RootMagisk.com Packages", "SamsungTool.us CellTool", "tojo360 Tool", "Knoxwizard Activation", "TFM Pro tool", "Taj AuthTool", "Gsmhelptool.com Activation", "GSMCode.Pro Tools", "MIFRPTOOL.COM", "Gsm Auth Tool", "Falcon FRP Tool", "Best Auth Tool", "mifrp Tool", "FAST FRP TOOL", "AI Tools", "Galaxy Auth", "E-GSM"],
  skus_affected=["Anonymouse Anynymouse Anonymous [xiaomiauth.org]Tool [AUTO API ] EXISTING USER", "Repair-Fix Xiaomi Auth Tool (RepairFixAuthTools.com) Credit AUTO API [EXISTING USER ]"],
  claim="The live reseller-pricing HTML names 22 tool-developer domains in SKU names (21 groups) (e.g. xiaomiauth.org, repairfixauthtools.com, radexfrp.com, tool.emmc-ufs.com, celltool.io), and two SKUs carry an explicit 'AUTO API' marker; no supplier/reseller domain appears anywhere in the HTML.",
  evidence_type="public JS/HTML", source_url="https://server.halabtech.com/resellerpricing/server",
  retrieved_utc="2026-10-11T10:12Z", excerpt="Anonymouse Anynymouse Anonymous [xiaomiauth.org]Tool [AUTO API ] EXISTING USER",
  access="full page", tool="mcp__Firecrawl__firecrawl_scrape", confidence="UNKNOWN",
  alternative_explanations="Domains identify the product's own web panel (where credits are loaded), not necessarily who sells HalabTech the credits; 'AUTO API' strings may be copied verbatim from an upstream Dhru catalog.",
  contradicting_evidence="none",
  what_would_confirm="developer pages offering a Dhru API to resellers and listing HalabTech; identical '[AUTO API ]' strings on a candidate supplier's catalog with lower prices",
  what_would_reject="the same strings appearing only on HalabTech-downstream servers",
  supports_or_contradicts="Complements R6 vendor lists (not previously captured as HTML evidence)",
  notes="Full list: gsmhelptool.com, knoxwizard.com, gsmcode.pro, radexfrp.com, rootmagisk.com, xiaomiauth.org, gsmauth.com, falconfrptool.com, mifrptool.com, bestauthtool.com, mifrp.com, fastfrptool.com, repairfixauthtools.com, samsungtool.us, celltool.io, whtai.co, tajtool.com, tojo360.com, tool.emmc-ufs.com, galaxy-realme.com, beta.tfmtool.com, egsmkey.com. Lead for catalog-genealogy streams: search '[AUTO API ]' with the space before ']' on other Dhru servers.")

f(tid="W1-13", entity="R3Tools and 'CU2@Gel' (method credits in HalabTech's own Windows tool)", entity_website="https://tools.halabtech.com/",
  role_for_halabtech="Content Partner", chain_layer="method authors -> HalabTech Tool (in-house software)", direction="R3Tools / CU2@Gel -> HalabTech",
  claim="tools.halabtech.com presents HalabTech's own 'Halabtech Tool' (v1.1, downloaded from support.halabtech.com) and its changelog credits R3Tools for the Samsung MTB FRP method and 'CU2@Gel' for test-point FRP.",
  evidence_type="public JS/HTML", source_url="https://tools.halabtech.com/",
  retrieved_utc="2026-10-11T10:11Z", excerpt="Add MTB Frp SAMSUNG (MOST Of Devices Supported) [All Thanks to R3Tools]",
  access="full page", tool="mcp__Firecrawl__firecrawl_scrape", confidence="CONFIRMED",
  alternative_explanations="Courtesy credits for publicly shared methods; no commercial supply relationship implied.",
  contradicting_evidence="none", what_would_confirm="n/a", what_would_reject="n/a",
  supports_or_contradicts="Supports OWN-05 (in-house products)",
  notes="Static page ('saved from url=https://tools.halabtech.com/vis/'), contact Halabtech.cert@gmail.com; download -> support.halabtech.com file id 212148; counters (374,917 users etc.) are self-reported.")

f(tid="W1-14", entity="htlinks.com / link.halabtech.com (HalabTech link hubs) and FRP-APK sources (romstage, addrom)", entity_website="https://htlinks.com/",
  role_for_halabtech="Not linked", chain_layer="n/a (free content links)", direction="n/a",
  claim="htlinks.com/frp (linked from halabtech.com's menu) redirects to the Firebase app halabfrp-be4d9.web.app ('HalabTechFRP' APK list) whose downloads point to frpbypass.romstage.com, addrom (GitHub) and similar free sources; htlinks.com itself is HalabTech's link hub, not an upstream platform.",
  evidence_type="public JS/HTML", source_url="https://htlinks.com/frp",
  retrieved_utc="2026-10-11T10:17Z", excerpt="HalabTechFRP APK Store",
  access="full page", tool="mcp__Firecrawl__firecrawl_scrape; mcp__Parallel_Search__web_fetch", confidence="CONFIRMED",
  alternative_explanations="n/a", contradicting_evidence="none", what_would_confirm="n/a", what_would_reject="n/a",
  supports_or_contradicts="New (negative for supply)",
  notes="Firecrawl metadata: sourceURL https://htlinks.com/frp -> url https://halabfrp-be4d9.web.app/. htlinks.com NS aragorn/eleanor.ns.cloudflare.com (different Cloudflare account from halabtech.com). link.halabtech.com = 'HALABTECH Files/Solutions Sender Tool' (earn points for uploading files). No payment/top-up aggregator or supplier links found on any HalabTech page; external links are social (t.me/HTSupport, t.me/halabtech2, wa.me/+963992951910, wa.me/+249116472371), dhru.com affiliate and joudisoft.com.")

f(tid="W1-15", entity="HalabTech World Agents 2019 (gsmfastest.com, mygsm24.com/mygsm24reseller.com, imeipk.com, safeunlocker.com, kbgsmstore.com, enesgsm.com, mehrinfo.net, unlockimei.us/imeishop.us, mundocelularstore.com, liderprogrammer.com, unlockinghn)", entity_website="https://support.halabtech.com/index.php?a=pages&b=world-agents",
  role_for_halabtech="Downstream Customer", chain_layer="HalabTech -> agents (support/membership packages)", direction="HalabTech -> agents",
  claim="The July 2019 World Agents page listed GSM shops in USA/India, Dominican Republic, Cuba, Mexico, Honduras, Venezuela, Pakistan, China, Nepal, Indonesia, UAE, Europe, UK, Iran and Turkey as HalabTech agents for paid support accounts - a downstream channel, not suppliers.",
  evidence_type="Wayback", source_url="https://web.archive.org/web/20190718171635/https://support.halabtech.com/index.php?a=pages&b=world-agents",
  retrieved_utc="2026-10-11T10:17Z", excerpt="Site: UNLOCKIMEI.US - www.imeishop.us",
  pub_date="2019-07-18", access="full page", tool="mcp__Parallel_Search__web_fetch", confidence="CONFIRMED",
  alternative_explanations="Some agents (e.g. GSMFastest, MyGSM24) are themselves distributors and could also sell to HalabTech in other product lines.",
  contradicting_evidence="none", what_would_confirm="n/a", what_would_reject="n/a",
  supports_or_contradicts="Supports D-17 and D-18 (current agent lists) with a 2019 baseline",
  notes="unlockimei.us / imeishop.us is NOT the candidate supplier imei.us. Personal phone numbers on the page were deliberately not copied. halabtech.com/resellers-halabtech/ (archived 2020-10-29, post dated 14/01/2017) lists city agents in Turkey, Egypt, Iraq, Lebanon, Yemen, Jordan, Sudan, Syria, Gaza, Saudi Arabia, Germany, Morocco, Algeria, Libya, UK - 'to activate paid accounts'.")

f(tid="W1-16", entity="GsmServer (reverse direction: sells HalabTech Platinum)", entity_website="https://gsmserver.com/en/halabtech-platinum",
  role_for_halabtech="Downstream Customer", chain_layer="HalabTech -> GsmServer (HalabTech membership resold)", direction="HalabTech -> GsmServer",
  claim="GsmServer has a product page 'Halabtech Platinum', i.e. it resells HalabTech's own membership, so the GsmServer-HalabTech relationship is two-way.",
  evidence_type="other", source_url="https://gsmserver.com/en/halabtech-platinum",
  retrieved_utc="2026-10-11T10:18Z", excerpt="Halabtech Platinum - GsmServer",
  access="search snippet", tool="mcp__Parallel_Search__web_search", confidence="STRONG",
  alternative_explanations="Page could be a stale listing; snippet only (page not fetched).",
  contradicting_evidence="none",
  what_would_confirm="fetch the page and read the product description/price", what_would_reject="page 404 or unrelated product",
  supports_or_contradicts="Supports D-17 (GsmServer listed among HalabTech world agents); context for V-10/W1-07",
  notes="Mutual trade complicates direction inference from shared catalog strings between HalabTech and GsmServer.")

f(tid="W1-17", entity="Candidate suppliers' infrastructure: code-gsm.com, unlockspro.com, gsmserver.com, imei.us, best4unlock.us", entity_website="",
  role_for_halabtech="Not linked", chain_layer="n/a (infrastructure context)", direction="n/a",
  claim="None of the candidate suppliers shares HalabTech's IPs, Cloudflare nameserver pair or hosting: code-gsm.com is on OVH (51.38.113.98), imei.us on Hetzner 95.216.43.145 with Namecheap DNS, and unlockspro.com, gsmserver.com and best4unlock.us sit behind separate Cloudflare accounts.",
  evidence_type="DNS/RDAP/CT", source_url="https://dns.google/resolve?name=imei.us&type=A (and A/NS for the other four)",
  retrieved_utc="2026-10-11T10:16Z", excerpt="{\"name\":\"imei.us.\",\"type\":1,\"TTL\":1800,\"data\":\"95.216.43.145\"}",
  access="JSON endpoint", tool="mcp__Parallel_Search__web_fetch (dns.google)", confidence="CONFIRMED",
  alternative_explanations="Infrastructure separation is expected even between real trading partners; it neither proves nor disproves supply.",
  contradicting_evidence="imei.us (95.216.43.145) is in the same Hetzner /16 as HalabTech's SPF IP 95.216.33.175 - a common hosting range, meaningless as evidence.",
  what_would_confirm="n/a", what_would_reject="n/a",
  supports_or_contradicts="Neutral for Code-GSM / UnlocksPro LIKELY hypotheses",
  notes="NS: code-gsm.com dns18/ns18.ovh.net; unlockspro.com rihana/chad.ns.cloudflare.com; gsmserver.com gloria/tom.ns.cloudflare.com; best4unlock.us lloyd/brianna.ns.cloudflare.com; imei.us dns1/dns2.registrar-servers.com. RDAP for these domains could not be retrieved (Parallel/Exa cannot parse application/rdap+json; rdap.org 404 for .us).")

f(tid="W1-18", entity="HalabTech subdomain inventory (CT current certs + Wayback 2015-2026)", entity_website="",
  role_for_halabtech="Not linked", chain_layer="n/a", direction="n/a",
  claim="About 45 HalabTech hostnames are visible (CT: chat, chatsosogsm, chatsosogsm2, chatmenet, aireply, agent, server, tools, store, admin.store, api.store; Wayback: course, digital, games, hardware, id, ip, link, pass, point, tool, techub, cert, forum, shop, demo, kontor, vb5 ...) and none is named after a supplier, API partner or white-label source.",
  evidence_type="DNS/RDAP/CT", source_url="https://api.certspotter.com/v1/issuances?domain=halabtech.com&include_subdomains=true&expand=dns_names&expand=issuer ; https://web.archive.org/cdx/search/cdx?url=halabtech.com&matchType=domain&collapse=urlkey",
  retrieved_utc="2026-10-11T10:15Z", excerpt="\"dns_names\": [ \"admin.store.halabtech.com\", \"api.store.halabtech.com\", \"www.admin.store.halabtech.com\", \"www.api.store.halabtech.com\" ]",
  access="JSON endpoint", tool="mcp__Parallel_Search__web_fetch", confidence="CONFIRMED",
  alternative_explanations="A wildcard certificate (*.halabtech.com via Cloudflare) hides proxied subdomains from CT; crt.sh history was unavailable, so older supplier-named hosts cannot be fully excluded.",
  contradicting_evidence="none",
  what_would_confirm="crt.sh full history when available", what_would_reject="a historical cert naming e.g. api.<supplier> or <partner>.halabtech.com",
  supports_or_contradicts="New",
  notes="Wayback roots with first-capture dates: accountsystem/acsy (2017-01), support (2017-04), cert (2017-05), forum (2017-06), up/qs (2017-04), demo/dm (2018-06), kontor (2018-07), server (2019-05), en/shop (2019-11), demo1/demo2/hardware (2020), pass (2021-08), course (2021-11), ip (2022-01), digital (2022-05), tool (2022-05), link (2022-07), id (2022-08), point (2023-03), tools (2023-08), games (2023-09), latest (2024-05), supportmail (2024-08), apps/host/vb5 (2024-12), store/api.store/admin.store (2025-01), news (2025-09), techub (2025-12), chat (2025-12). CertSpotter issuers: Cloudflare (SSL.com/Google TS), Let's Encrypt (cPanel AutoSSL on tools./store.).")

f(tid="W1-19", entity="JoudiSoft - Real Easy Store (support.halabtech.com software)", entity_website="https://joudisoft.com/products/real-easy-store/",
  role_for_halabtech="Platform", chain_layer="n/a (download-store software)", direction="JoudiSoft -> HalabTech (software licence)",
  claim="support.halabtech.com's footer credits JoudiSoft's Real Easy Store, its JS config exposes a standard userapi endpoint, and its sitemap index covers only downloads (116 file sitemaps + 7 core URLs), with no server/IMEI products.",
  evidence_type="public JS/HTML", source_url="https://support.halabtech.com/ ; https://support.halabtech.com/sitemap.xml",
  retrieved_utc="2026-10-11T10:19Z", excerpt="'userapi': 'https://support.halabtech.com/userapi/index.php'",
  access="full page", tool="mcp__Firecrawl__firecrawl_scrape; mcp__Parallel_Search__web_fetch", confidence="CONFIRMED",
  alternative_explanations="n/a", contradicting_evidence="none", what_would_confirm="n/a", what_would_reject="n/a",
  supports_or_contradicts="Confirms brief (support = Real Easy Store); adds vendor JoudiSoft",
  notes="robots.txt disallows /userapi/ and /admin/ and blocks GPTBot, Amazonbot, AhrefsBot, SemrushBot etc. JSON-LD = Organization/WebSite/WebPage only. Menu links to hardware.halabtech.com and pass.halabtech.com. The /userapi/ endpoint was not called.")

negative_findings = [
    {"entity": "crt.sh (Certificate Transparency history)", "url": "https://crt.sh/?q=%25.halabtech.com&output=json", "what_was_checked": "full CT history for *.halabtech.com", "result": "unavailable: 502 Bad Gateway (Exa 10:10Z, Firecrawl 10:12Z and 10:19Z), Parallel timeout 10:11Z; substituted CertSpotter (current certs only) + Wayback host list", "tool": "mcp__Exa__web_fetch_exa; mcp__Firecrawl__firecrawl_scrape; mcp__Parallel_Search__web_fetch"},
    {"entity": "Public code (GitHub/gists/READMEs)", "url": "firecrawl_developer_search / Exa / Parallel", "what_was_checked": "repos, gists, READMEs or integration guides naming halabtech, server.halabtech.com, HTSupport, HALABTECHSupportbot or HalabTech as Dhru API source/client", "result": "none; only HalabTech's own pages, a Kodular Play-store wrapper app (io.kodular.dabodgaming.HalabTech), a webcompat issue and generic dhru-com repos", "tool": "mcp__Firecrawl__firecrawl_developer_search x2; mcp__Exa__web_search_exa; mcp__Parallel_Search__web_search"},
    {"entity": "Tracking-ID pivots", "url": "web search for ca-pub-9647107642564560 / G-3FW622FWW6", "what_was_checked": "other domains sharing HalabTech analytics/AdSense IDs", "result": "no other domain found (IDs not indexed by search engines)", "tool": "mcp__Parallel_Search__web_search"},
    {"entity": "Sitemaps", "url": "server./support./news./store./halabtech.com sitemaps", "what_was_checked": "whether sitemaps expose server/IMEI product pages or name a source", "result": "server.halabtech.com/sitemap.xml 404 (Dhru), store 403, /en/wp-sitemap.xml 503; support = downloads only; halabtech.com 142 post sitemaps + 14 pages; news 33 post sitemaps; no product pages, no supplier names", "tool": "mcp__Parallel_Search__web_fetch; mcp__Firecrawl__firecrawl_scrape"},
    {"entity": "robots.txt", "url": "https://support.halabtech.com/robots.txt etc.", "what_was_checked": "hidden paths / sitemap pointers revealing partners", "result": "nothing supplier-related; server. has no robots.txt (404), tools. is an SPA catch-all, store allows all", "tool": "mcp__Parallel_Search__web_fetch"},
    {"entity": "Third-party chat / pixel vendors", "url": "all HalabTech home pages", "what_was_checked": "Tawk, Crisp, Tidio, Facebook pixel, GTM, Yandex, Clarity, Hotjar IDs", "result": "none present; chat is in-house (n8n webhook)", "tool": "mcp__Firecrawl__firecrawl_scrape"},
    {"entity": "store.halabtech.com front-end JS", "url": "https://store.halabtech.com/build/assets/app-D2jpX1vH.js", "what_was_checked": "API base URLs / third-party services in public JS", "result": "only axios 1.6.8 bundle; no endpoints", "tool": "mcp__Firecrawl__firecrawl_scrape"},
    {"entity": "Wayback keyword search halabtech.com/*", "url": "https://web.archive.org/cdx/search/cdx?url=halabtech.com/*&filter=original:.*(api|source|supplier|partner|agent|distribut|reseller|dhru|wholesale|vendor|provider).*", "what_was_checked": "archived blog URLs about suppliers, API docs or partners", "result": "only firmware posts (api = Samsung build code), resellers-halabtech/ and resellers-qtool-turkey/ (2017)", "tool": "mcp__Parallel_Search__web_fetch"},
    {"entity": "RDAP for supplier domains", "url": "https://rdap.org/domain/<code-gsm.com|unlockspro.com|gsmserver.com|imei.us|best4unlock.us>", "what_was_checked": "registrar/creation dates", "result": "not retrieved: Parallel fetch_error (application/rdap+json), Exa CRAWL_UNEXPECTED_CONTENT_TYPE, rdap.org 404 for .us; DNS A/NS obtained instead", "tool": "mcp__Parallel_Search__web_fetch; mcp__Exa__web_fetch_exa"},
    {"entity": "HTD white-label siblings", "url": "Exa search", "what_was_checked": "other GSM stores built on htdtech.dev", "result": "none surfaced", "tool": "mcp__Exa__web_search_exa"},
    {"entity": "Candidate supplier names on HalabTech pages", "url": "server./support./news./store./tools./halabtech.com home + resellerpricing/server + pid=4113", "what_was_checked": "any mention or link to code-gsm, unlockspro, imei.us, best4unlock, sickw or other server suppliers", "result": "none; only developer domains inside SKU names and dhru.com affiliate link", "tool": "mcp__Firecrawl__firecrawl_scrape"},
]

new_leads = [
    "SosoGSM (sosogsm.net / support.sosogsm.net): chatsosogsm(.2).halabtech.com certs (2026-08-29) imply a HalabTech-hosted chatbot for SosoGSM - compare SosoGSM's Dhru catalog strings/prices with HalabTech to set direction.",
    "chatmenet.halabtech.com (certs 2026-09-03): identify the 'menet' client.",
    "HTD (htdtech.dev, t.me/HTDtechdev, +90 WhatsApp): determine whether HTD is HalabTech-owned; check whether store.halabtech.com's 82 'Activation | Credits Tools' items are synced via Dhru API from server.halabtech.com or another upstream (price comparison).",
    "2020 archived catalogs (Wayback 2020-05-31 IMEI, 2020-06-02 server): match 'SOURCE A/B', '#S1-#S4', '1250# iP Gsx Check', 'From Gsx Checker', 'Infinity online services2 ... AUTO API' against 2020 captures of candidate suppliers to name the sources.",
    "Search other Dhru servers for the exact strings '[xiaomiauth.org]Tool [AUTO API ]' and 'RepairFixAuthTools.com) Credit AUTO API [EXISTING USER ]' (space before ']') to find the upstream catalog they were copied from.",
    "Fetch https://gsmserver.com/en/halabtech-platinum to confirm GsmServer resells HalabTech memberships (two-way relationship).",
    "Wayback https://server.halabtech.com/sitemap.xml (2023-07-21, 200) was not fetched (Parallel 429) - may list Dhru service URLs/pids from 2023.",
    "Retry crt.sh later for full CT history (older subdomains could reveal partner names).",
]

open_questions = [
    "Is server.halabtech.com self-hosted on the Layout-Team/Hetzner server 95.216.33.175 (SPF evidence) rather than Dhru cloud? (affects whether API logs/suppliers could be inferred from hosting - they cannot from public data).",
    "Does 'HTD' (store platform) belong to HalabTech, and does the store resell server.halabtech.com services via Dhru API?",
    "Which upstream sources correspond to HalabTech's 2020 labels (Source A/B, S1-S4, Supplier 3) and are they the same as today's 'Source 1#/2#/3#'?",
    "Did GsmServer remain a supplier for Octoplus after the 'GsmServer Products' group disappeared (Octoplus lists HalabTech as an official reseller)?",
]

out_obj = {"stream": "W1-web-infra", "generated_utc": "2026-10-11T10:25Z", "tool_log": tool_log, "findings": F,
           "negative_findings": negative_findings, "new_leads": new_leads, "open_questions": open_questions,
           "raw_captures_dir": raw_dir,
           "redaction_note": "Client-side chat API key values (server./support. widgets) and the halabtech.com guest widget token were redacted in saved raw captures and never used; personal phone numbers from archived agent pages were not copied into findings."}
json.dump(out_obj, open(out, 'w'), ensure_ascii=False, indent=1)
print('findings', len(F), 'tool_log', len(tool_log), 'negatives', len(negative_findings))
for x in F:
    assert len(x['excerpt'].split()) <= 25, (x['tid'], len(x['excerpt'].split()))
print('excerpt lengths ok')
