"""Round-7 curated knowledge (hand-curated from findings W1-W7 + V7; see findings/*.json for the raw stream output).

Everything here references stream finding IDs (tids such as 'W4-07'); curate_r7.py maps them to Evidence-Registry IDs
(EV-267+). Raw stream files are never modified; Phase-5 corrections are applied only to the curated copy and logged.
"""

# --------------------------------------------------------------------------------------------------------------
# 1. Phase-5 corrections to stream findings (applied to the curated copy only; originals kept in findings/*.json)
# --------------------------------------------------------------------------------------------------------------
MINIUTES = ("'Miniutes' is a Dhru platform default (W6 negative check: it appears on unrelated Dhru servers such as "
            "xpertunlock, best4unlock, idunlocker), so it is withdrawn as a HalabTech genealogy marker.")
CORRECTIONS = [
    dict(tid='V7-11', field='claim', reason=MINIUTES + ' Confidence unchanged: HalabTech-proprietary products, the '
         "'Sliver' typo and contiguous import blocks remain.",
         new="Live Firecrawl scrape (W3 used Exa) shows UnlocksPro selling HalabTech's memberships/credits/support "
             "(#22876-22887, with HalabTech's 'Sliver' typo) and a group literally named 'GsmServer Products' with "
             "HalabTech's 'Boot-Loader 2.0 Activation Code (100 days, 7 GB)' item - UnlocksPro imports HalabTech's catalogue."),
    dict(tid='W7-05', field='claim', reason=MINIUTES + ' Discount range corrected by V7-18 (second-tool re-fetch).',
         new="HOS Unlocker resells HalabTech-proprietary products (support.halabtech.com credits, HALABTECH memberships, "
             "HalabTech's 'TEST API CODE') at 2.8-12.5% below HalabTech's public list. So HOS is a HalabTech dealer, and "
             "HalabTech's public price list is not its dealer price."),
    dict(tid='W7-06', field='claim', reason=MINIUTES,
         new="Eagle Unlocker sells HalabTech's PSN UK SKUs, including the 'Bound' (for Pound) typo, at exactly HalabTech's "
             "10:03Z public price x 1.05 (32.49 -> 34.115; 45.98 -> 48.279)."),
    dict(tid='W7-10', field='entity', reason=MINIUTES,
         new="Downstream cluster carrying HalabTech digital-goods names and typos ('Bound', '(Turkey Users)', "
             "'Giving Code NOT By Player ID', '( Unknown Cash ) (AUTO API)')"),
    dict(tid='W7-10', field='claim', reason=MINIUTES,
         new="At least 25 Dhru servers carry HalabTech's exact digital-goods names or group names. Several show "
             "HalabTech-only products ('Key Credits Halabtech' at gsmserver24) or known downstream status (3gsm.ru is a "
             "HalabTech World Agent), consistent with API import from HalabTech."),
    dict(tid='W7-03', field='what_would_confirm', reason=MINIUTES,
         new="GsmUnlockingstore prices equal to HalabTech's price x a constant (as for W7-06/07/08), or its service list "
             "carrying HalabTech-only items (HALABTECH memberships, HalabTech Point, TEST API SKUs)."),
    dict(tid='W7-08', field='notes', reason=MINIUTES, replace=("Delivery strings 'Miniutes' copied.",
         "(Delivery string 'Miniutes' is a Dhru default and is not used as evidence.)")),
    dict(tid='W7-16', field='alternative_explanations', reason=MINIUTES, replace=(
         "etunlocker shows 'Miniutes' (HalabTech-downstream marker).",
         "('Miniutes' on etunlocker is a Dhru default, not a HalabTech marker.)")),
    dict(tid='W3-03', field='claim', conf='DISPUTED',
         reason="Date misread: GSM-Forum prints MM-DD-YYYY, so '04-02-2026' is 2 April 2026, not 4 February (V7-08). The "
                "timing premise is reversed; HalabTech's 2 Mar 2026 batch is the earliest dated appearance.",
         new="Code-GSM's GSM-Forum thread with the exact 'Till 17 Series [ Clean & Paid Off Only ]' name is dated "
             "04-02-2026 = 2 April 2026 (MM-DD-YYYY), not 4 February. HalabTech's 10 Feb 2026 catalog had no such group "
             "and HalabTech added the tiers in one batch on 2 Mar 2026, so the dated record shows HalabTech first and the "
             "copy direction is not established."),
    dict(tid='W2-14', field='alternative_explanations', conf='UNKNOWN',
         reason="Tier-discount caveat: HalabTech dealers sell 2.8-12.5% below HalabTech's public list (V7-18, W7-05), so "
                "competitors at $16.00-17.20 may be HalabTech dealers; price neither supports nor refutes HalabTech's "
                "'direct source' claim. The price observation itself stands.",
         append=" Phase 5: HalabTech's own dealers undercut its public list by 2.8-12.5% (V7-18), so lower competitor "
                "prices are not evidence against HalabTech being the source."),
    dict(tid='W6-08', field='alternative_explanations', conf='DISPUTED',
         reason="Direction contradicted for the Mi Account family: Code-GSM carries HalabTech's internal routing label "
                "'Source2 #Cheaper' and malformed braces (V7-10, W2-09), and HalabTech dealers undercut its list (V7-18). "
                "The FMI OFF family traces to GSM Nigeria -> Code-GSM (+$2.00, W6-10).",
         append=" Phase 5: Code-GSM imports HalabTech-internal labels (V7-10), so being cheaper does not make it upstream."),
    dict(tid='W4-09', field='notes', conf='DISPUTED',
         reason="Rejected by V7-07: the store 'Details: api' / 'AUTO API' label also appears on HalabTech's own "
                "server-balance vouchers, so it marks the store's link to HalabTech's own Dhru server, not an external supplier.",
         append=" Phase 5: hypothesis rejected (V7-07)."),
    dict(tid='W4-10', field='notes', conf='LIKELY',
         reason="Second-tool re-check failed: the live Hydra shop (Exa, 10:51Z) shows only $10/$15/$25/$40 packages, not the "
                "$1.00/credit retail quoted from a Parallel search snippet (V7-16). Without the vendor-retail leg the STRONG "
                "upgrade is unsupported; R6 LIKELY (agent listing) stands.",
         append=" Phase 5: vendor per-credit retail not re-confirmed (V7-16); kept at LIKELY."),
    dict(tid='W6-04', field='claim', reason="Precision: the constant multiplier is x1.0217, not x1.022 (V7-20, live Firecrawl).",
         replace=("x1.022", "x1.0217")),
    dict(tid='W3-13', field='claim', reason="Logic: a downstream customer for some products can still be upstream for others, so "
         "UnlocksPro is unlikely - not impossible - as the Signal Labs source.",
         replace=("from a supplier that cannot be UnlocksPro if W3-09/W3-10 hold.",
                  "from an unidentified supplier; UnlocksPro is downstream of HalabTech for server products and shared IMEI "
                  "names (W3-09/W3-10), so it is an unlikely source unless the two trade reciprocally.")),
    dict(tid='W2-03', field='alternative_explanations', conf='UNKNOWN',
         reason="Both HalabTech prices in the ratio test (28.49, 9.99) are manual 'charm' prices, not computed markups, and "
                "x1.425 lies outside HalabTech's observed computed-markup range (x1.025-1.30, V7-03); W2-03's own "
                "contradicting evidence shows other MDM SKUs do not fit. A two-point ratio is not a fingerprint.",
         append=" Phase 5: both HalabTech prices are manual charm prices, so the shared ratio is likely coincidental."),
    dict(tid='W6-11', field='notes', reason="Live re-read failed: gsmfather.com/resellerpricing/imei now 404s (V7-21); evidence "
         "rests on Exa's capture. Confidence unchanged (LIKELY).",
         append=" Phase 5: page 404 on live re-check (V7-21); single-tool evidence."),
]

# --------------------------------------------------------------------------------------------------------------
# 2. Route types used in the Service Inventory (for metrics)
# --------------------------------------------------------------------------------------------------------------
ROUTES = {
    'IN': 'In-house (HalabTech)',
    'VR': 'Vendor rule: developer -> HalabTech direct',
    'VD': 'Vendor direct (developer lists HalabTech)',
    'VA': 'Vendor direct via vendor reseller/DHRU API',
    'NI': 'Named intermediary (distributor / API supplier)',
    'LC': "Vendor's listed channel (member unnamed)",
    'FP': 'Named candidate by price/ID fingerprint',
    'NS': 'Unnamed numbered source (HalabTech label)',
    'UK': 'Unknown',
    'DS': 'Disputed candidate',
}

# --------------------------------------------------------------------------------------------------------------
# 3. Group-level R7 assessments (overrides on top of R6 / W5 automatic rules)
#    keys: dev, dev_url, status, cand, route, conf, tids, note
# --------------------------------------------------------------------------------------------------------------
NCK_FU = dict(cand="Fast Unlocking (fastunlocking.co.uk, 'NCK & UMT Team Activation Server', first UMT worldwide distributor) - "
                   "named candidate; other UMT/NCK distributors (GsmServer, GsmEasy, Martview) price above HalabTech",
              route='NI', conf='LIKELY', tids=['W4-07', 'V7-15'],
              note='R6 named 7 possible distributors; R7 narrows to Fast Unlocking on public prices (same confidence).')
FG = dict(cand="An unnamed Furious Gold distributor (HalabTech's $0.878 credit undercuts every public offer: GsmServer $1.00, "
               "gsmfather $0.88, fmifix $0.907, centerunlock $0.96, unlockresellers $0.97)",
          route='LC', conf='LIKELY', tids=['W4-08'], note='Unchanged vs R6 (REL-086).')
DC = dict(route='VD', conf='LIKELY', tids=['W4-20'],
          note="Price ($0.61) inside the public reseller band; 'DC Unlocker Dongle 2 Year Support' listed twice ($17.99 and "
               "computed $18.313) suggests two parallel sources.")
HYD = dict(route='VD', conf='LIKELY', tids=['W4-10', 'V7-16', 'V7-19'],
           note="W4-10 proposed STRONG (prices below retail); Phase 5 could not re-confirm vendor retail (V7-16) -> R6 LIKELY kept. "
                "GSM Nigeria uses HalabTech's group typo 'Hydra Digital Actiavtion' (V7-19).")
OCTO = dict(dev='Octoplus Box team', dev_url='https://octoplusbox.com', status='Official reseller (worldwide block and Turkey; R6 A1-10)',
            cand='Octoplus team direct (official reseller; $0.10 shared reseller credit cost, HalabTech x1.07)',
            route='VD', conf='LIKELY', tids=['W5-71', 'W4-15'],
            note='R6 linked the vendor (VEN-003) but not these groups; R7 maps them.')
SIG = dict(cand="GsmServer - Sigma's exclusive distributor; resellers fund the Sigma panel by buying credits on GsmServer's website (tiers $0.87/0.85/0.83 bracket HalabTech's costs)",
           route='VR', conf='STRONG', tids=['W4-04', 'V7-27', 'W1-07', 'V7-12'], note='Unchanged STRONG (REL-027); 2020 history added.')
TMOB_PREM_NOTE = ("Both SKUs moved by the same ratio between 02:00 and 10:03 UTC; prices resolve to round upstream costs $115.00/"
                  "$125.00 at x1.06 -> x1.045. No public seller at $115/$125 found (GSMUnlockUSA 108.95/114.95/149.95; "
                  "GsmUnlockingStore $90-96; GSMFATHER 4002# $127).")
DIGI = "Digital goods: names are HalabTech's own (cannot fingerprint upstream); "

GROUP_OVR = {
    # ---- in-house / internal -------------------------------------------------------------------------------
    'GRP-S-247': dict(route='IN', conf='CONFIRMED', tids=['W4-22', 'W1-16', 'W3-06', 'W6-15', 'W7-05', 'V7-18', 'V7-11', 'W6-06'],
                      note='Own memberships/credits; resold by GsmServer, Code-GSM, UnlocksPro, HOS, WARD, MrUnlockers, Fix4GSM and others.'),
    'GRP-S-093': dict(route='IN', conf='CONFIRMED', tids=['W6-02', 'W6-03', 'W6-05'], note="Internal transfer SKU; mirrored by MW Unlocker, GSM Tiger, Saudi-GSM."),
    'GRP-S-092': dict(route='IN', conf='CONFIRMED', tids=[], note='Own file-request service (R6).'),
    'GRP-S-236': dict(route='IN', conf='CONFIRMED', tids=['W6-16', 'W6-01'], note='Own bundles; retired bundles still mirrored by the gsmtiger/reunlocker/mwunlocker cluster.'),
    'GRP-S-234': dict(route='IN', conf='CONFIRMED', tids=['W6-05', 'V7-18'], note="Internal test SKUs; 'TEST API CODE' resold by Saudi-GSM (x1.1) and HOS ($0.1)."),
    'GRP-I-031': dict(route='IN', conf='CONFIRMED', tids=['W6-01', 'W6-04', 'V7-20'], note="'TEST API IMEI' mirrored by ReUnlocker and univgsm (x1.08)."),
    'GRP-S-136': dict(dev='HalabTech (in-house n8n chat / RAG)', dev_url='https://server.halabtech.com', status='Own product',
                      cand='In-house (HalabTech operates the bot; buyers likely SosoGSM and "menet" via chat*.halabtech.com)',
                      route='IN', conf='LIKELY', tids=['V7-22', 'W1-04', 'W1-06'], note='New in R7: product reinterpreted as in-house.'),
    'GRP-S-260': dict(dev='HTD (htdtech.dev) - store SaaS used by store.halabtech.com', dev_url='https://htdtech.dev/',
                      status='Reseller of HTD plans (ownership link to HalabTech unproven)',
                      cand='HTD vendor direct - or in-house if HTD is HalabTech-owned (unproven)', route='VD', conf='LIKELY',
                      tids=['W1-03', 'W6-06'], note='UnlocksPro resells the HTD plans in a block with HalabTech products.'),
    # ---- vendor-rule STRONG (unchanged) ---------------------------------------------------------------------
    'GRP-S-072': dict(**SIG),
    'GRP-S-252': dict(cand="GsmServer at the top of the chain (Sigma's exclusive distributor); immediate seller may be a GsmServer "
                           "sub-reseller (HalabTech = x1.10 of $54.00/$40.50; GsmEasy near-match)",
                      route='VR', conf='STRONG', tids=['W4-05', 'W4-04'], note='Unchanged STRONG for GsmServer as source of Sigma products.'),
    'GRP-S-242': dict(cand="Chimera distributor tier: GsmEasy (imei.us), GsmServer or Unlock.eu - all sell reseller credits at $0.092; "
                           "HalabTech prices = x1.080-1.088 of credit-denominated licences",
                      route='VR', conf='STRONG', tids=['W4-01', 'W4-02', 'W4-03', 'V7-13'],
                      note='Unchanged STRONG that HalabTech buys via a Chimera distributor; candidate set widened to 3 (Unlock.eu).'),
    'GRP-S-264': dict(route='VR', conf='STRONG', tids=['V7-04'], note='Re-verified: 3 WorldWide distributors (HalabTech, Easy Team, HALIUNLOCK); no direct sales to agents.'),
    'GRP-S-182': dict(route='VR', conf='STRONG', tids=['V7-05'], note='Re-verified: 3 WorldWide distributors (GSM-T-TOOL, Hali-Unlock, HalabTech).'),
    'GRP-S-189': dict(route='VR', conf='STRONG', tids=[], note='Unchanged (REL-085).'),
    # ---- named intermediaries / channels --------------------------------------------------------------------
    'GRP-S-052': dict(**NCK_FU), 'GRP-S-104': dict(**NCK_FU), 'GRP-S-244': dict(**NCK_FU), 'GRP-S-314': dict(**NCK_FU),
    'GRP-S-313': dict(**NCK_FU),
    'GRP-S-248': dict(**FG), 'GRP-S-279': dict(**FG),
    'GRP-S-240': dict(cand="An EFT distributor (Easy Team/Easy-Unlocker - also HalabTech's co-distributor at Hunter - or SimSim, "
                           "GsmServer, GSM-Sources, MartView, SharkGSM, GsmEasy, GsmFastest); no candidate price fits >=2 SKUs",
                      route='LC', conf='LIKELY', tids=['W4-06', 'V7-04'], note='Unchanged (REL-093).'),
    'GRP-S-253': dict(conf='UNKNOWN', route='UK', tids=['W4-16'],
                      cand='Direct (Cheetah reseller account) or a Cheetah distributor; HalabTech sells at 92.6-97.9% of distributor retail',
                      note='Unchanged UNKNOWN.'),
    'GRP-S-218': dict(route='LC', conf='LIKELY', tids=['W4-13'], note='GsmServer excluded at public prices (HalabTech implied cost $0.76 < $0.80).'),
    'GRP-S-259': dict(route='LC', conf='LIKELY', tids=['W4-13'], note='GsmServer excluded at public prices (HalabTech implied cost $0.76 < $0.80).'),
    'GRP-S-243': dict(**DC), 'GRP-S-317': dict(**DC), 'GRP-S-318': dict(**DC),
    'GRP-S-112': dict(route='VD', conf='LIKELY', tids=['W4-19'], note='No public seller matches implied TSM credit cost $0.75 (x1.30).'),
    'GRP-S-059': dict(**HYD), 'GRP-S-193': dict(**HYD), 'GRP-S-278': dict(**HYD),
    'GRP-S-214': dict(cand='Dhru Cloud or a Dhru distributor (e.g. GSM Africa); add-on ratios inconsistent (1.21/1.024/1.297)',
                      route='LC', conf='LIKELY', tids=['W4-21', 'W7-17'], note='Resale CONFIRMED (D-29, W7-17); source unresolved.'),
    'GRP-S-258': dict(route='VD', conf='LIKELY', tids=['W4-17'], note='HalabTech prices = list minus pennies; GsmEasy $42.20 non-discriminating.'),
    'GRP-S-213': dict(route='VD', conf='LIKELY', tids=['W4-18'], note="ADY reuses HalabTech's DFT strings (downstream)."),
    'GRP-S-167': dict(route='VD', conf='LIKELY', tids=['W4-18'], note="ADY reuses HalabTech's FlexUnlock strings (downstream)."),
    'GRP-S-012': dict(dev='Cerberus Tool (Cerberus Tool Pro / Tool Box)', dev_url='https://cerberustoolpro.com/partners',
                      status='Special Distributor (listed first of 6; top tier with ADYunlocker, TEAM UNLOCK)',
                      cand="Cerberus vendor direct via its DHRU-compatible seller API", route='VA', conf='LIKELY',
                      tids=['W5-69', 'W5-72', 'V7-02', 'V7-17'],
                      note='SKUs renamed 02:00->10:03 UTC to vendor product names (API name-sync fits); prices are not one markup '
                           'over vendor public prices (W5-72 contradiction).'),
    'GRP-S-232': dict(cand='Sim-Unlocker Pro vendor reseller API (HalabTech listed as reseller)', route='VA', conf='LIKELY',
                      tids=['W5-09', 'W5-73']),
    'GRP-S-069': dict(cand='Apizu vendor Reseller API for Dhru Fusion (HalabTech in SUPER PREMIUM tier)', route='VA', conf='LIKELY',
                      tids=['W5-22', 'W5-74']),
    'GRP-S-263': dict(cand="CF Tools channel: AppleUnlockers (single Main Distributor) above HalabTech (Worldwide Reseller), or a "
                           "direct reseller account", route='NI', conf='LIKELY', tids=['W5-21', 'W5-75']),
    'GRP-S-319': dict(cand="CF Tools channel: AppleUnlockers (single Main Distributor) above HalabTech (Worldwide Reseller), or a "
                           "direct reseller account", route='NI', conf='LIKELY', tids=['W5-21', 'W5-75']),
    'GRP-S-203': dict(cand="Tira channel: HalabTech holds a reseller listing; ADY Unlocker is the sole distributor above resellers",
                      route='NI', conf='LIKELY', tids=['W5-05', 'W5-78']),
    'GRP-S-276': dict(cand='Fast Unlocker Pro vendor direct (HalabTech listed distributor); ADY Unlocker WhatsApp receives direct-sale payments',
                      route='VD', conf='LIKELY', tids=['W5-07', 'W5-78'],
                      note="GSM Nigeria 0.57 vs HalabTech implied 0.56 - no exact match (W6-09 notes)."),
    'GRP-S-109': dict(dev='GsmAuth.com (Sohaib Akram)', dev_url='https://www.gsmauth.com/', status='Not listed (no public list)',
                      cand="GsmDone.com - declared by GsmAuth as the Dhru Web API partner for credit recharge", route='NI',
                      conf='LIKELY', tids=['W5-76'], note='HalabTech SKU priced $0 at 10:03Z (probably disabled).'),
    'GRP-S-233': dict(dev='SETool team', dev_url='https://files.setool.net/support/SETool2/', status='Not listed',
                      cand='GsmEasy - the only distributor named on the official SETool support page', route='NI', conf='LIKELY',
                      tids=['W5-77'], note='Support page is old (SETool2); may be outdated for the LG tool.'),
    'GRP-S-262': dict(dev='Alseery Unlocker', status='Vendor site unreachable (W5)',
                      cand='GSM Nigeria (gsmnigeria.com) - sells both SKUs at $0.68 = HalabTech implied cost (HalabTech $0.748 = x1.10); direction unresolved',
                      route='FP', conf='LIKELY', tids=['W6-09', 'V7-19']),
    'GRP-S-096': dict(dev='F-KEY TOOL', status='No public list (W5)',
                      cand='GSM Nigeria (gsmnigeria.com) - sells both SKUs at $1.08 = HalabTech implied cost (HalabTech $1.134 = x1.05); direction unresolved',
                      route='FP', conf='LIKELY', tids=['W6-09', 'V7-19']),
    'GRP-S-250': dict(dev='Infinity-Box team (SKU names: "iNfinity Laelo Samsung Unlock tool")', dev_url='https://infinity-box.com',
                      status='7. Distributor (Infinity; R6 EV-067/EV-199)',
                      cand='Infinity-Box team direct (HalabTech is an official Infinity distributor)', route='VD', conf='LIKELY',
                      tids=[], note='Attribution to Infinity rests on HalabTech\'s SKU wording; Laelo not seen on the vendor site in R7.'),
    # ---- vendor lists that omit HalabTech (W5 ABSENT) -------------------------------------------------------
    'GRP-S-024': dict(cand='Via MIUI Tool\'s only listed resellers: Dost Service or IMEI ve SERVER (Turkey)', route='NI', conf='LIKELY', tids=['W5-90']),
    'GRP-S-041': dict(cand='Via FRP BRASIL (Worldwide Distributor) or supremegsm (listed reseller)', route='NI', conf='LIKELY', tids=['W5-87']),
    'GRP-S-120': dict(cand="Via one of Lazy Loader's 15 listed (mostly Indian) resellers - member unnamed", route='LC', conf='LIKELY', tids=['W5-82']),
    'GRP-S-126': dict(cand='Owner/main distributor direct (only channel listed) - account not listed', route='LC', conf='LIKELY', tids=['W5-87']),
    'GRP-S-156': dict(cand='Owner/main distributor direct (only channel listed) - account not listed', route='LC', conf='LIKELY', tids=['W5-87']),
    'GRP-S-158': dict(cand='Via a listed KrakenAuth distributor (Kibe_r007, Soul Unlocker, FixPhone) - Soul Unlocker is the lead', route='LC', conf='LIKELY', tids=['W5-52']),
    'GRP-S-161': dict(cand="Via a listed TONI reseller (akgsmserver, Leope-Gsm, Soso GSM, cleanunlocker, ...); note HalabTech hosts chat "
                           "sub-domains for SosoGSM (V7-22)", route='LC', conf='LIKELY', tids=['V7-22']),
    'GRP-S-162': dict(cand='3gsm.ru - sole Xiaomi Flasher Pro distributor (also a HalabTech World Agent: two-way)', route='NI', conf='LIKELY', tids=['W7-10']),
    'GRP-S-181': dict(cand='Via a listed Xiaomi Paid Tool distributor (iphoneunlockingstore, Offlock, ohideraunlocker, ...) - member unnamed', route='LC', conf='LIKELY', tids=['W5-86']),
    'GRP-S-209': dict(cand='Via GSM-Sources (listed ZXW distributor) or HAOFANG COMMUNICATION', route='NI', conf='LIKELY', tids=[]),
    'GRP-S-210': dict(cand='Via a Wuxinji regional channel (Global/Vietnam/India/Bangladesh/Iraq/Indonesia/Malaysia) - member unnamed', route='LC', conf='LIKELY', tids=[]),
    'GRP-S-299': dict(cand='Via a listed MFC dealer (GsmServer, GSM-Sources, ARTGSM, EOEM)', route='LC', conf='LIKELY', tids=[]),
    'GRP-S-226': dict(cand='Via ADY Unlocker (only worldwide reseller) or GsmServer HK (listed reseller)', route='NI', conf='LIKELY', tids=['W5-78', 'W5-88']),
    'GRP-S-300': dict(cand='Via ADY Unlocker (listed worldwide) or another listed GuerraTool reseller', route='NI', conf='LIKELY', tids=['W5-78', 'W5-88']),
    'GRP-S-019': dict(cand='Unresolved: vendor sells direct (5/30/50 USDT; HalabTech prices below that) and lists only East-African resellers',
                      route='UK', conf='UNKNOWN', tids=['W5-92']),
    'GRP-S-025': dict(cand='Unresolved: vendor also sells credits directly; listed distributors Easy Admin, HEART UNLOCK', route='UK', conf='UNKNOWN', tids=[]),
    'GRP-S-026': dict(cand="Unresolved: Smartbe Unlock (primary distributor, direct API) / Clean Unlocker Team, or an unlisted API-integration account",
                      route='UK', conf='UNKNOWN', tids=['W5-80']),
    # ---- other UNKNOWN groups with R7 work --------------------------------------------------------------------
    'GRP-S-110': dict(cand='Unresolved (distributor names not rendered); lead: Soul Unlocker (Kraken Big Distributor)', route='UK', conf='UNKNOWN', tids=[]),
    'GRP-S-095': dict(cand='Unresolved; lead: HaliUnlock sells QCDMA TOOL (Yemen)', route='UK', conf='UNKNOWN', tids=['W5-81']),
    'GRP-S-297': dict(cand='Unresolved; lead: HaliUnlock sells CDMA_YEMEN_TOOL; UnlocksPro resells HalabTech\'s CDMA YEMEN block (downstream)',
                      route='UK', conf='UNKNOWN', tids=['W5-81', 'W6-06']),
    'GRP-S-102': dict(cand='Unresolved; lead: HaliUnlock (Yemeni tool family distributor)', route='UK', conf='UNKNOWN', tids=['W5-81']),
    'GRP-S-227': dict(dev='Wondershare (Dr.Fone)', dev_url='https://drfone.wondershare.com', status='No public reseller list',
                      cand="Unresolved: name family shared by >=12 servers; '- Ready Account' variants and two cheaper peers (gsmgenesis, grandunlock)",
                      route='UK', conf='UNKNOWN', tids=['W7-16']),
    'GRP-S-293': dict(cand="Unresolved; lead: Layout Team (HalabTech's own hosting provider per SPF/DNS) - not shown to supply hosting for resale",
                      route='UK', conf='UNKNOWN', tids=['W1-02']),
    # ---- digital goods ------------------------------------------------------------------------------------
    'GRP-S-080': dict(dev='Syriatel (official recharge denominations)', dev_url='https://www.syriatel.sy/services/denominations-of-recharging-cards',
                      cand='Unidentified recharge channel; HalabTech holds Syriatel Cash/MTN Cash/Sham Cash wallets - manual or self-fulfilled recharge fits better than an API',
                      route='UK', conf='UNKNOWN', tids=['W7-01', 'W7-02']),
    'GRP-S-081': dict(cand='Unidentified recharge channel (manual/self-fulfilled fits best)', route='UK', conf='UNKNOWN', tids=['W7-02']),
    'GRP-S-085': dict(cand=DIGI + 'PayCell/Turkcell/TT prices manual or stale', route='UK', conf='UNKNOWN', tids=['W7-13']),
    'GRP-S-086': dict(cand=DIGI + 'PayCell/Turkcell/TT prices manual or stale', route='UK', conf='UNKNOWN', tids=['W7-13']),
    'GRP-S-087': dict(cand=DIGI + 'PayCell/Turkcell/TT prices manual or stale', route='UK', conf='UNKNOWN', tids=['W7-13']),
    'GRP-S-220': dict(cand=DIGI + 'all 6 prices = face TL x 0.021174 USD (47.227 TRY/USD): a face-value-linked TRY e-pin source '
                           '(candidates Turkpin, Oyuneks, Pinmarkt, ExePin) - unnamed', route='UK', conf='UNKNOWN', tids=['W7-13']),
    'GRP-S-221': dict(cand=DIGI + 'iTunes-TR prices manual or stale; source unnamed', route='UK', conf='UNKNOWN', tids=['W7-13', 'W7-07']),
    'GRP-S-204': dict(cand=DIGI + 'gift-card distributor unidentified', route='UK', conf='UNKNOWN', tids=['W7-14', 'W7-06', 'W7-07']),
    'GRP-S-256': dict(cand=DIGI + 'gift-card distributor unidentified', route='UK', conf='UNKNOWN', tids=['W7-14']),
    'GRP-S-257': dict(cand=DIGI + 'implied $27.80/100 AED and $13.90/50 AED (0.278 USD/AED); distributor unidentified', route='UK', conf='UNKNOWN', tids=['W7-14']),
    'GRP-S-230': dict(cand=DIGI + "delivered from HalabTech's own pre-bought code stock; wholesaler unidentified", route='UK', conf='UNKNOWN', tids=['W7-04', 'W7-10', 'W7-08']),
    'GRP-S-237': dict(cand=DIGI + "delivered from HalabTech's own pre-bought code stock; wholesaler unidentified", route='UK', conf='UNKNOWN', tids=['W7-04', 'W7-03', 'W7-09']),
    'GRP-S-238': dict(cand=DIGI + "'(AUTO API)' direct top-up via several sources ('Server # 3', '{Vietnam ONLY}'); 60 UC $0.927 = $0.90 x1.03; FazerCards ($0.80) does not match",
                      route='NS', conf='UNKNOWN', tids=['W7-11', 'W7-12', 'W7-09']),
    'GRP-S-172': dict(cand=DIGI + 'manual delivery (1-24 h) consistent with AI-account wholesalers (sans.uz, s-ai.live, ggsel sellers) - unnamed',
                      route='UK', conf='UNKNOWN', tids=['W7-15']),
    # ---- IMEI -------------------------------------------------------------------------------------------------
    'GRP-I-000': dict(cand='Unidentified API supplier (implied costs $17.95/$21.95/$4.50/$5.53 at x1.15-1.25); UnlocksPro withdrawn as candidate (downstream)',
                      route='UK', conf='UNKNOWN', tids=['W3-13', 'W3-11'], note='R6 LIKELY rested on UnlocksPro as candidate upstream (REL-098), now reversed.'),
    'GRP-I-008': dict(cand='Unnamed premium source selling at $115.00 / $125.00 (price fingerprint)', route='UK', conf='UNKNOWN',
                      tids=['V7-01', 'W2-04', 'W2-05', 'W2-06', 'W2-07'], note=TMOB_PREM_NOTE),
    'GRP-I-009': dict(cand='Unresolved; Best4unlock is a sibling (33 shared names incl. "Prheck" typo; 8 tiny checks within rounding of HalabTech implied costs)',
                      route='UK', conf='UNKNOWN', tids=['W6-13', 'W3-10']),
    'GRP-I-012': dict(cand='HalabTech self-claims to be the direct source (Source #1); downstream servers (UnlocksPro #25579-83) import the group with HalabTech\'s label',
                      route='IN', conf='LIKELY', tids=['W6-07', 'W2-01', 'W2-14', 'W2-03'],
                      note='Self-claim only; competitor prices $16.00-17.20 do not test it (dealer tiers, V7-18).'),
    'GRP-I-013': dict(cand='Unresolved (UnlocksPro withdrawn as candidate: downstream)', route='UK', conf='UNKNOWN', tids=['W3-10', 'W6-06']),
    'GRP-I-016': dict(cand='Unresolved; unlockresellers resells the SKU at HalabTech x1.125 (downstream)', route='UK', conf='UNKNOWN', tids=['W6-17']),
    'GRP-I-017': dict(cand="Unnamed 'Source 3#' for the current Android-17 SKU; GsmUnlockingStore is a LIKELY candidate only for the retired "
                           "April-2026 'LEVEL 5' batch", route='NS', conf='UNKNOWN', tids=['V7-14', 'W2-02', 'W2-01']),
    'GRP-I-018': dict(cand="Disputed: Code-GSM (HalabTech = Code-GSM + whole dollars, identical cents) vs a common upstream (TinUnlock carries "
                           "the names under another server's IDs 3277#-3281#; Code-GSM buys T-Mobile from 'supplier#2' 3708#); HalabTech posted first (2 Mar 2026)",
                      route='DS', conf='DISPUTED', tids=['V7-08', 'W2-08', 'W3-01', 'W3-02', 'W3-03', 'W3-07', 'W3-08', 'W6-12', 'W3-04'],
                      note='R6 LIKELY (REL-097) -> DISPUTED.'),
    'GRP-I-019': dict(cand='Unresolved: iRemove partner channel; GSM Nigeria -> Code-GSM (+$2.00) cluster sells the family; HalabTech offsets not constant',
                      route='UK', conf='UNKNOWN', tids=['W2-12', 'W6-10', 'W6-08']),
    'GRP-I-020': dict(cand='Unresolved: iRemove partner channel; GSM Nigeria -> Code-GSM (+$2.00) cluster sells the family; HalabTech offsets not constant',
                      route='UK', conf='UNKNOWN', tids=['W2-12', 'W6-10', 'W6-08']),
    'GRP-I-023': dict(cand="Unnamed 'Source #2' / 'Source #3' (candidates: tecnomdm.com $9.59 vs $9.79; GsmUnlockingStore '[ Source 2 ]' $7.00) - neither fits",
                      route='NS', conf='UNKNOWN', tids=['W2-13', 'W2-03', 'W2-15', 'W2-01']),
    'GRP-I-025': dict(cand="Unnamed numbered Samsung FRP sources (four parallel sources announced 2025-04-11)", route='NS', conf='UNKNOWN', tids=['W2-01']),
    'GRP-I-028': dict(dev='Orange Moldova (carrier unlock)', cand="GSMFATHER (embeds its own service IDs; 1351#/1352# carried in HalabTech's names) or the "
                           "upstream behind GSMFATHER's NNNN# numbering", route='FP', conf='LIKELY', tids=['W6-11', 'V7-21', 'V7-20'],
                      note='New in R7 (was UNKNOWN). GSMFATHER page now 404 - single-tool evidence.'),
    'GRP-I-036': dict(cand="Unnamed numbered routes ('Server Direct', 'Source2 #Cheaper', Source 1#/2#/3#); naming originates at HalabTech; Code-GSM is downstream",
                      route='NS', conf='UNKNOWN', tids=['W2-09', 'V7-10', 'W2-17', 'W2-01']),
    'GRP-I-040': dict(cand="Unidentified 2020 GSX upstream whose IDs survive as '#225', '#33225' and '32596' (in HalabTech names since 2020)",
                      route='UK', conf='UNKNOWN', tids=['W2-10', 'W2-11', 'W1-08']),
    'GRP-I-045': dict(cand='Unresolved; GX Unlocker reuses all 10 names (downstream)', route='UK', conf='UNKNOWN', tids=['W6-14']),
    'GRP-I-047': dict(cand='Unresolved EDL/CPID operator (candidates nevutek.com, server.imeishop.net, serverunlocker.com); univgsm resells at x1.0217 (downstream)',
                      route='UK', conf='UNKNOWN', tids=['W2-16', 'V7-20']),
    'GRP-I-048': dict(cand="Unresolved JDM operator; UnlocksPro withdrawn (it copied HalabTech's 'Netowrk' names by 2024)", route='UK', conf='UNKNOWN',
                      tids=['W3-10', 'W6-14', 'W2-16']),
    'GRP-I-050': dict(cand="Unresolved CPID operator; lead: GSM Nigeria's 'SAMSUNG Repair Netowrk ... CPID Services - Direct Distributor' group (placeholder only)",
                      route='UK', conf='UNKNOWN', tids=['V7-19', 'W2-16']),
    'GRP-I-051': dict(cand="Unresolved CPID operator; lead: GSM Nigeria's 'SAMSUNG Repair Netowrk ... CPID Services - Direct Distributor' group (placeholder only)",
                      route='UK', conf='UNKNOWN', tids=['V7-19', 'W2-16']),
    'GRP-I-056': dict(cand="Unresolved CPID operator; lead: GSM Nigeria's 'SAMSUNG Repair Netowrk ... CPID Services - Direct Distributor' group (placeholder only)",
                      route='UK', conf='UNKNOWN', tids=['V7-19', 'W2-16']),
    'GRP-I-054': dict(cand='Unresolved (UnlocksPro withdrawn: it used HalabTech\'s group by 2023)', route='UK', conf='UNKNOWN', tids=['W3-10']),
}
for _g in ('GRP-S-170', 'GRP-S-206', 'GRP-S-215', 'GRP-S-251', 'GRP-S-288', 'GRP-S-289', 'GRP-S-290', 'GRP-S-291'):
    GROUP_OVR[_g] = dict(**OCTO)

# issuer brands for digital-goods groups (identity only; not research sources)
for _g, _dev in {'GRP-S-204': 'Sony Interactive Entertainment (PlayStation Store)', 'GRP-S-256': 'Apple (App Store & iTunes gift cards)',
                 'GRP-S-257': 'Apple (App Store & iTunes gift cards)', 'GRP-S-221': 'Apple (App Store & iTunes gift cards)',
                 'GRP-S-220': 'Google (Google Play gift codes)', 'GRP-S-237': 'Krafton / Level Infinite (PUBG Mobile)',
                 'GRP-S-238': 'Krafton / Level Infinite (PUBG Mobile)', 'GRP-S-230': 'Garena (Free Fire)', 'GRP-S-081': 'MTN Syria (operator)',
                 'GRP-S-085': 'Paycell (Turkcell group)', 'GRP-S-086': 'Turkcell (operator)', 'GRP-S-087': 'Turk Telekom (operator)',
                 'GRP-S-080': 'Syriatel (operator)'}.items():
    GROUP_OVR.setdefault(_g, {}).update(dev=_dev, issuer_known=True)
GROUP_OVR['GRP-S-250']['ev_extra'] = 'EV-067; EV-199 (Infinity listing, R6)'

# SKU-level overrides inside mixed groups: (group_id, substring of service name) -> fields
SKU_OVR = [
    ('GRP-I-018', 'System Check', dict(cand="Unidentified source of the 'System Check (Fully Paid - Eligible)' family (also on UnlocksPro #25743 and "
                                             "gsmunlockers.com, whose tiers are x1.35 of whole-dollar costs $22/26/41/57)",
                                        route='UK', conf='UNKNOWN', tids=['W3-07', 'V7-09'])),
]

# --------------------------------------------------------------------------------------------------------------
# 4. Supplier Intelligence register (entities). ids: existing SUP-/VEN- ids where they exist; new SUP-031+ / CUS-001+
# --------------------------------------------------------------------------------------------------------------
E = lambda **k: k
ENTITIES = [
    # --- upstream candidates (supplier side) ---
    E(id='SUP-001', name='GsmServer (gsmserver.com)', url='https://gsmserver.com', type='Master Distributor; Intermediate Supplier; also Downstream reseller',
      rel="Sigma's exclusive distributor -> HalabTech (STRONG); one of three Chimera distributor-tier sources (STRONG-shared); "
          "'GsmServer Products' group in HalabTech's catalog 2020-2024 (STRONG, historical); listed MFC/TheMagicTool reseller; "
          "sells HalabTech's own memberships (downstream, CONFIRMED)",
      direction='GsmServer -> HalabTech (Sigma, historical GsmServer Products); HalabTech -> GsmServer (memberships)',
      groups=['GRP-S-072', 'GRP-S-252', 'GRP-S-242', 'GRP-S-299', 'GRP-S-226'], r6='STRONG (Sigma); STRONG-shared (Chimera); LIKELY (GsmServer Products)',
      r7='STRONG (Sigma; GsmServer Products 2020-24); STRONG-shared (Chimera); CONFIRMED downstream reseller', tids=['W4-04', 'V7-27', 'W4-05', 'W4-01', 'W4-03', 'W1-07', 'V7-12', 'W4-22', 'W1-16'],
      alt='HalabTech may buy Sigma activations from a GsmServer sub-reseller (GsmEasy near-match).', contra='GsmServer public retail is above HalabTech for Sigma activations, Global Unlocker, Furious Gold, UMT (non-public tiers needed).',
      confirm='GsmServer or HalabTech naming the account; panel-credit invoice patterns.', reject='Sigma naming another distributor; HalabTech Sigma prices below GsmServer panel tiers.'),
    E(id='SUP-012', name='GsmEasy (imei.us / gsmeasyshop.com)', url='https://www.imei.us/', type='Master Distributor; Intermediate Supplier',
      rel='One of three Chimera distributor-tier sources ($0.092); sole SETool distributor named by SETool (LIKELY for Setool); Sigma activation near-match; UMT public price above HalabTech',
      direction='GsmEasy -> HalabTech (candidate)', groups=['GRP-S-242', 'GRP-S-233', 'GRP-S-252'],
      r6='STRONG-shared (Chimera)', r7='STRONG-shared (Chimera); LIKELY (SETool)', tids=['W4-01', 'V7-13', 'W5-77', 'W4-05', 'W4-17'],
      alt='HalabTech could buy SETool via a GsmEasy reseller.', contra='GsmEasy UMT 1Y $23.00 is above HalabTech $22.85 (excluded for UMT at public price).',
      confirm='GsmEasy naming HalabTech as client; matching price moves.', reject='Chimera/SETool naming another source for HalabTech.'),
    E(id='SUP-013', name='Unlock.eu', url='https://unlock.eu/', type='Master Distributor (Chimera "Distributor" card)',
      rel='Sells Chimera reseller packs at exactly $0.092/credit - equally price-consistent third Chimera source', direction='Unlock.eu -> HalabTech (hypothesis)',
      groups=['GRP-S-242'], r6='UNKNOWN', r7='UNKNOWN (one of 3 price-consistent sources)', tids=['W4-02'],
      alt='', contra='Chimera text names only two distributors (CL-021).', confirm='Chimera or Unlock.eu naming HalabTech.', reject='Chimera confirming only GsmEasy/GsmServer.'),
    E(id='SUP-017', name='Fast Unlocking (fastunlocking.co.uk / .com)', url='https://www.fastunlocking.co.uk/', type='Master Distributor; API Supplier (NCK & UMT team activation server)',
      rel="UMT's first worldwide distributor and 'NCK & UMT Team Activation Server' with 'direct support to all other servers APIs'; the only UMT/NCK/AVB seller "
          "whose public prices sit at or just below HalabTech's", direction='Fast Unlocking -> HalabTech (candidate)',
      groups=['GRP-S-052', 'GRP-S-104', 'GRP-S-244', 'GRP-S-314', 'GRP-S-313'], r6='UNKNOWN (one of 7 named UMT distributors)', r7='LIKELY',
      tids=['W4-07', 'V7-15'], alt='Another UMT distributor with non-public API pricing.', contra='', confirm='Fast Unlocking API price list = HalabTech cost / markup for >=3 SKUs.',
      reject='HalabTech UMT prices below Fast Unlocking reseller prices.'),
    E(id='SUP-014', name='Code-GSM (code-gsm.com; GSM Tool v2 platform)', url='https://www.code-gsm.com/', type='Downstream Customer; disputed API Supplier',
      rel="Imports HalabTech's Mi Account family (internal label 'Source2 #Cheaper', malformed braces) and resells HalabTech memberships (STRONG downstream); "
          "upstream role for 'T-Mobile Clean & Paid Off' DISPUTED (HalabTech posted first; price structure fits Code-GSM->HalabTech or a common upstream)",
      direction='HalabTech -> Code-GSM (Mi Account, memberships); Code-GSM <-> HalabTech (T-Mobile Clean, disputed)',
      groups=['GRP-I-036', 'GRP-S-247', 'GRP-I-018', 'GRP-I-019', 'GRP-I-020'], r6='LIKELY (T-Mobile; price conflict CL-013)',
      r7='STRONG (downstream); DISPUTED (T-Mobile upstream)', tids=['V7-10', 'W2-09', 'W3-06', 'V7-08', 'W2-08', 'W3-01', 'W3-02', 'W6-08', 'W6-10'],
      alt='Bilateral exchange: each imports some services from the other.', contra='HalabTech = Code-GSM + whole dollars with identical cents (W3-01).',
      confirm='A dated Code-GSM listing before 2 Mar 2026, or Code-GSM naming HalabTech as supplier/client.', reject='Code-GSM first-appearance after HalabTech for every shared family.'),
    E(id='SUP-015', name='UNLOCKSPRO Premium Server (unlockspro.com)', url='https://unlockspro.com/', type='Downstream Customer',
      rel="Resells HalabTech-proprietary products in contiguous import blocks (memberships #22876-87 with 'Sliver' typo, HTD plans, DHRU bundle, CDMA YEMEN) and "
          "HalabTech's 'MDM Source 1#' group; IMEI names copied since 2023", direction='HalabTech -> UnlocksPro',
      groups=['GRP-S-247', 'GRP-S-260', 'GRP-I-012', 'GRP-I-048', 'GRP-I-054', 'GRP-I-000', 'GRP-I-013'], r6='LIKELY (candidate upstream; direction unproven)',
      r7='STRONG (downstream, server); LIKELY (downstream, IMEI); upstream hypothesis DISPUTED', tids=['W3-09', 'W3-10', 'W3-11', 'W6-06', 'W6-07', 'V7-11'],
      alt='Reciprocal partner for a few IMEI items (e.g. Signal Labs) cannot be excluded.', contra='', confirm='', reject='HalabTech names carrying UnlocksPro IDs.'),
    E(id='SUP-031', name='GSM Nigeria (gsmnigeria.com, "The Wholesale Unlocking Source")', url='https://www.gsmnigeria.com/', type='Intermediate Supplier (candidate); also Downstream reseller',
      rel="Sells Alseery ($0.68) and F-KEY ($1.08) exactly at HalabTech's implied costs; 140 exact HalabTech server names, cheaper on 142/150; shares HalabTech's group typo "
          "'Hydra Digital Actiavtion'; sells HalabTech credits at $0.97; feeds Code-GSM's FMI OFF family (+$2.00)",
      direction='GSM Nigeria -> HalabTech (Alseery, F-KEY; candidate); HalabTech -> GSM Nigeria (HalabTech credits)', groups=['GRP-S-262', 'GRP-S-096', 'GRP-S-278', 'GRP-I-019', 'GRP-I-020'],
      r6='-', r7='LIKELY (two SKU families); direction unresolved overall', tids=['W6-09', 'W6-10', 'V7-19'],
      alt='Common upstream at 0.68/1.08; GSM Nigeria could be a large HalabTech dealer.', contra='GSM Nigeria resells HalabTech credits (downstream for those).',
      confirm='Dated first appearance of shared names/typos; synchronous price moves.', reject='HalabTech price history at the same cost basis predating GSM Nigeria.'),
    E(id='SUP-032', name='GSMFATHER (gsmfather.com)', url='https://www.gsmfather.com/', type='API Supplier (candidate); also HalabTech product reseller',
      rel="Its own service IDs 1351#/1352# are embedded in HalabTech's Moldova SKU names; sells 'HalabTech Credits' and has a 'gsm server products' category",
      direction='GSMFATHER (or its upstream) -> HalabTech (Moldova)', groups=['GRP-I-028'], r6='-', r7='LIKELY (Moldova only; not a general upstream: 4 shared names of 705)',
      tids=['W6-11', 'V7-21'], alt="The NNNN# numbering may belong to an upstream shared by GSMFATHER and the Dhru demo shop ('1342#').", contra='Price page now 404 (single-tool evidence).',
      confirm='GSMFATHER Telegram/new-storefront record for IDs 1351/1352.', reject='An older server carrying 1351#/1352# Moldova before GSMFATHER.'),
    E(id='SUP-033', name='GsmUnlockingStore (gsmunlockingstore.com; GUSTORE)', url='https://gsmunlockingstore.com/', type='API Supplier (candidate); Reseller (peer); Downstream for some items',
      rel="Announced HalabTech's exact 'SAMSUNG FRP ... LEVEL 5' names the same day HalabTech posted them as 'Source #3' (Apr 2026); claims 'DIRECT SOURCE' for a T-Mobile "
          "family (prices do not fit); resells HalabTech-style PUBG code names", direction='two-way / unresolved',
      groups=['GRP-I-017', 'GRP-I-023', 'GRP-I-012', 'GRP-I-019', 'GRP-I-020', 'GRP-S-237'], r6='(listed in SUP-028 downstream)',
      r7='LIKELY (historical Samsung FRP Source #3 batch); UNKNOWN (MDM, T-Mobile, FMI)', tids=['V7-14', 'W2-02', 'W2-03', 'W2-05', 'W2-12', 'W7-03'],
      alt='Common upstream; or GUS importing from HalabTech.', contra='HalabTech posted ~5 h before GUS\'s forum post; GUS buys HalabTech products.',
      confirm='GUS IDs or labels inside HalabTech SKU names.', reject='HalabTech names predating GUS for the LEVEL 5 family.'),
    E(id='SUP-034', name='tecnomdm.com ("Tecno MDM"; footer t.me/GSMManager)', url='https://tecnomdm.com/', type='API Supplier (candidate)',
      rel="Sells a business-days-only Tecno/Itel/Infinix MDM unlock at $9.59 vs HalabTech 'Source #2' $9.79", direction='tecnomdm -> HalabTech (candidate)',
      groups=['GRP-I-023'], r6='-', r7='UNKNOWN', tids=['W2-13'], alt='Several Monday-to-Friday MDM offers exist; near price may be coincidence.',
      contra='Delivery differs (1-7 vs 1-3 days).', confirm='Price moves in step with HalabTech Source #2.', reject='HalabTech Source #2 older than tecnomdm.'),
    E(id='SUP-035', name='gsmunlockers.com (reseller) / unnamed upstream at $22/$26/$41/$57', url='https://gsmunlockers.com/', type='Reseller (peer); points to an unnamed upstream',
      rel="Guest prices for T-Mobile 'Fully Paid / Eligible' tiers = x1.35 of whole-dollar costs $22/$26/$41/$57 - fingerprint of a cheaper upstream; carries HalabTech's "
          "'System Check (Fully Paid - Eligible)' string", direction='unnamed upstream -> gsmunlockers; relation to HalabTech UNKNOWN',
      groups=['GRP-I-018'], r6='-', r7='UNKNOWN (lead)', tids=['V7-09', 'W3-07'], alt='', contra='', confirm='A server publicly pricing these tiers at $22/26/41/57.', reject=''),
    E(id='SUP-036', name='GsmDone.com', url='https://www.gsmauth.com/', type='API Supplier (vendor-declared Dhru Web API partner)',
      rel="GsmAuth.com states GsmDone provides the Dhru Web API other websites use to recharge GsmAuth credits", direction='GsmDone -> HalabTech (candidate)',
      groups=['GRP-S-109'], r6='-', r7='LIKELY', tids=['W5-76'], alt='GsmAuth may also sell directly.', contra='HalabTech SKU priced $0 (disabled?).',
      confirm='GsmDone catalogue entry with the same name/price basis.', reject='HalabTech naming another source.'),
    E(id='SUP-037', name='AppleUnlockers (Gsm Anik)', url='https://appleunlockers.com', type='Master Distributor (CF Tools Main Distributor)',
      rel="CF Tools names AppleUnlocker its single Main Distributor and HalabTech a 'Worldwide Reseller'", direction='AppleUnlockers -> HalabTech (candidate)',
      groups=['GRP-S-263', 'GRP-S-319'], r6='-', r7='LIKELY', tids=['W5-75', 'W5-21'], alt='Direct reseller account created by the developer.', contra='',
      confirm='Vendor stating HalabTech sits under AppleUnlockers.', reject='Developer stating HalabTech is a direct reseller.'),
    E(id='SUP-018', name='ADY Unlocker (adyunlocker.com)', url='https://www.adyunlocker.com/', type='Intermediate Supplier (candidate); Reseller (peer); Downstream catalog consumer',
      rel="Sole Tira distributor (HalabTech reseller-tier); only worldwide reseller of TheMagicTool/GuerraTool; receives Fast Unlocker Pro payments; Cerberus co-Special "
          "Distributor; sole Panda distributor; reuses HalabTech DFT/FlexUnlock strings (downstream); same PUBG promo family", direction='two-way',
      groups=['GRP-S-203', 'GRP-S-226', 'GRP-S-300', 'GRP-S-306', 'GRP-S-213', 'GRP-S-167'], r6='LIKELY (Panda); UNKNOWN (others)',
      r7='LIKELY (Tira, Magic, Guerra, Panda channel); LIKELY downstream (DFT/FlexUnlock strings)', tids=['W5-78', 'W5-05', 'W5-88', 'W4-18', 'W7-12'],
      alt='HalabTech holds direct accounts at Tira/Fast Unlocker Pro.', contra='HalabTech is itself a listed Fast Unlocker Pro distributor.',
      confirm="ADY catalogue strings/prices identical to HalabTech's Tira/Magic/Guerra SKUs.", reject='Vendor statements that HalabTech buys direct.'),
    E(id='SUP-038', name='Smartbe Unlock (smartbeunlock.com)', url='https://www.mysteriofrp.com/', type='Master Distributor (Mysterio primary wholesale, direct API)',
      rel='Mysterio FRP omits HalabTech; names Smartbe Unlock its primary wholesale distributor with direct API (plus Clean Unlocker Team)', direction='Smartbe -> HalabTech (candidate)',
      groups=['GRP-S-026'], r6='-', r7='UNKNOWN', tids=['W5-80'], alt='Unlisted Mysterio API-integration account.', contra='', confirm="Smartbe catalogue with HalabTech's '[AUTO API]' wording.", reject=''),
    E(id='SUP-023', name='Hali-Unlock (haliunlock.com, Yemen)', url='https://haliunlock.com', type='Co-distributor (peer); candidate supplier for Yemeni tools',
      rel='Co-distributor with HalabTech at Hunter and Q-Unlocker; sells QCDMA TOOL and CDMA_YEMEN_TOOL; part of the Yemeni distributor pool',
      direction='peer; Hali-Unlock -> HalabTech (candidate for QCDMA/CDMA Yemen)', groups=['GRP-S-095', 'GRP-S-297', 'GRP-S-102'], r6='UNKNOWN', r7='UNKNOWN (lead)',
      tids=['V7-04', 'V7-05', 'W5-81'], alt='', contra='', confirm='HalabTech QCDMA/CDMA prices = Hali-Unlock price x markup.', reject=''),
    E(id='SUP-025', name='Easy Team / Easy-Unlocker (easy-unlocker.com, Iraq)', url='https://easy-unlocker.com', type='Master Distributor (EFT official); co-distributor (peer)',
      rel="EFT's 'official distributor in the world' and HalabTech's co-distributor at Hunter Unlocker", direction='Easy Team -> HalabTech (EFT candidate)',
      groups=['GRP-S-240', 'GRP-S-264'], r6='LIKELY (one of EFT channels)', r7='LIKELY (one of EFT channels)', tids=['V7-04', 'W4-06'],
      alt='Another EFT distributor.', contra='No EFT distributor price fits >=2 HalabTech SKUs.', confirm='EFT channel price sheet matching HalabTech.', reject=''),
    E(id='SUP-039', name='3gsm.ru', url='https://3gsm.ru', type='Master Distributor (XFP sole distributor); Downstream (HalabTech World Agent)',
      rel='Sole Xiaomi Flasher Pro distributor (HalabTech absent from XFP list); also lists HalabTech digital goods and is a HalabTech World Agent', direction='two-way',
      groups=['GRP-S-162'], r6='-', r7='LIKELY (XFP)', tids=['W7-10'], alt='', contra='', confirm='3gsm.ru XFP price x markup = HalabTech.', reject=''),
    E(id='SUP-040', name='Soul Unlocker (soulunlocker.com)', url='https://soulunlocker.com', type='Master Distributor (KrakenAuth Big Distributor; MULTIPROTOOL distributor)',
      rel='Candidate for KRAKEN AUTH and Soul Auth Tool SKUs', direction='Soul Unlocker -> HalabTech (candidate)', groups=['GRP-S-158', 'GRP-S-110'], r6='-', r7='UNKNOWN (lead)',
      tids=['W5-52'], alt='', contra='', confirm='', reject=''),
    E(id='SUP-002', name='DOSTService (dostservice.com)', url='https://dostservice.com', type='Distributor (Turkey); peer', rel='Only MIUI Tool reseller besides IMEI ve SERVER; HalabTech agent (R6)',
      direction='Dost Service -> HalabTech (MIUI Tool candidate)', groups=['GRP-S-024'], r6='CONFIRMED (peer listing)', r7='LIKELY (MIUI Tool channel)', tids=['W5-90'],
      alt='', contra='', confirm='', reject=''),
    E(id='SUP-007', name='GSM-Sources / SharkGSM', url='https://gsm-sources.com', type='Distributor', rel='Listed ZXW distributor and MFC dealer; EFT distributor', direction='candidate',
      groups=['GRP-S-209', 'GRP-S-299', 'GRP-S-240'], r6='UNKNOWN', r7='LIKELY-shared (ZXW, MFC channels)', tids=[], alt='', contra='', confirm='', reject=''),
    E(id='SUP-041', name='FRP BRASIL', url='https://tunaprotool.com/', type='Distributor (Tuna Pro Tool Worldwide Distributor)', rel='Candidate for Tuna Pro Tool', direction='candidate',
      groups=['GRP-S-041'], r6='-', r7='LIKELY-shared', tids=['W5-87'], alt='', contra='', confirm='', reject=''),
    E(id='SUP-042', name='GSM Manager (t.me/GSMManager)', url='https://opluspro.net', type='Master Distributor (OPlusPro/FalconMultiTool); peer',
      rel="Main Distributor of OPlusPro and FalconMultiTool (where HalabTech is a separate 'Distributor WorldWide'); buys HalabTech credits (R6 D-22); tecnomdm.com footer links t.me/GSMManager",
      direction='peer / unresolved', groups=['GRP-S-077', 'GRP-S-116', 'GRP-I-023'], r6='(D-22 downstream buyer)', r7='UNKNOWN', tids=['W5-79', 'W2-13'], alt='', contra='', confirm='', reject=''),
    E(id='SUP-043', name='Unnamed T-Mobile premium source ($115 / $125)', url='', type='API Supplier (unnamed)', rel='Price fingerprint: both Premium SKUs = $115.00/$125.00 x markup (x1.06 -> x1.045)',
      direction='unnamed -> HalabTech', groups=['GRP-I-008'], r6='UNKNOWN', r7='UNKNOWN (fingerprint CONFIRMED as fact)', tids=['V7-01', 'W2-04', 'W2-05'],
      alt='', contra='', confirm='A server publicly pricing the two services at $115/$125.', reject=''),
    E(id='SUP-044', name='Unidentified GSX upstream (#225 / #33225 / 32596)', url='', type='API Supplier (unnamed, since 2020)', rel="Upstream service IDs embedded in HalabTech's GSX names since 2020",
      direction='unnamed -> HalabTech', groups=['GRP-I-040'], r6='UNKNOWN', r7='UNKNOWN', tids=['W2-10', 'W1-08'], alt='', contra='', confirm='Server with native IDs 225/33225/32596.', reject=''),
    E(id='SUP-045', name='Unidentified NNNN#-B upstream (IDs 3277#-3281#)', url='https://tinunlock.com/resellerpricing/imei', type='API Supplier (unnamed)',
      rel="TinUnlock carries the T-Mobile Clean & Paid Off names under another server's IDs 3277#-3281#; possible common upstream of HalabTech and Code-GSM",
      direction='unnamed -> (Code-GSM, HalabTech?)', groups=['GRP-I-018'], r6='-', r7='UNKNOWN', tids=['W6-12', 'W3-04'], alt='', contra='', confirm='', reject=''),
    E(id='SUP-046', name='Unnamed numbered IMEI sources (Source #1/#2/#3/#4, Server Direct)', url='https://t.me/halabtech2', type='API Suppliers (unnamed)',
      rel="HalabTech's own labels and Telegram show >=4 parallel numbered sources (2020: Source A/B, S1-S4; 2024-26: Source #1-#4, 'SYNC API')",
      direction='unnamed -> HalabTech', groups=['GRP-I-017', 'GRP-I-023', 'GRP-I-025', 'GRP-I-036', 'GRP-I-021'], r6='CONFIRMED (existence)', r7='CONFIRMED (existence); identities UNKNOWN',
      tids=['W2-01', 'W1-08'], alt='Numbers may be separate products at one supplier.', contra='', confirm='', reject=''),
    # --- developers / vendors with notable R7 status ---
    E(id='VEN-081', name='Cerberus Tool (cerberustoolpro.com)', url='https://cerberustoolpro.com/partners', type='Original Developer (vendor with DHRU-compatible seller API)',
      rel="Lists HALABTECH first as 'Special Distributor'; offers sellers a DHRU-compatible API; HalabTech's SKU names synced to vendor product names between snapshots",
      direction='Cerberus -> HalabTech', groups=['GRP-S-012'], r6='Not checked', r7='CONFIRMED (authorisation); LIKELY (API fulfilment)', tids=['W5-69', 'W5-72', 'V7-02', 'V7-17'],
      alt='Manual rename to match vendor relaunch.', contra='Prices not one markup over vendor public prices.', confirm='Vendor API product names/IDs = HalabTech SKU strings.', reject='HalabTech SKUs matching another Cerberus distributor.'),
    E(id='VEN-016', name='Hydra Tool team (hydradongle.com)', url='https://srv.hydradongle.com/shop', type='Original Developer', rel='HalabTech is a documented Hydra agent (R6); credit prices below GsmServer retail',
      direction='Hydra team -> HalabTech', groups=['GRP-S-059', 'GRP-S-193', 'GRP-S-278'], r6='CONFIRMED (agent status); LIKELY (supply)', r7='CONFIRMED (agent status); LIKELY (supply)',
      tids=['W4-10', 'V7-16'], alt='', contra='Vendor per-credit retail not re-confirmed (V7-16).', confirm='', reject=''),
    E(id='VEN-045/046', name='Hunter Unlocker Pro / Q-Unlocker Pro', url='https://hunter-unlocker.com', type='Original Developer (sells only via 3 distributors)',
      rel='HalabTech is one of three WorldWide distributors of each; no direct sales to agents (re-verified R7)', direction='vendor -> HalabTech (direct)',
      groups=['GRP-S-264', 'GRP-S-182'], r6='STRONG', r7='STRONG', tids=['V7-04', 'V7-05'], alt='', contra='', confirm='Vendor statement naming HalabTech accounts as API-linked.', reject=''),
    E(id='VEN-020', name='SigmaKey team', url='https://sigmakey.com/en/content/15258', type='Original Developer', rel='Names GsmServer its exclusive distributor',
      direction='Sigma -> GsmServer -> HalabTech', groups=['GRP-S-072', 'GRP-S-252'], r6='CONFIRMED (exclusive distributor)', r7='CONFIRMED (exclusive distributor)', tids=['W4-04'], alt='', contra='', confirm='', reject=''),
    E(id='VEN-002', name='ChimeraTool', url='https://chimeratool.com/resellers', type='Original Developer', rel='Resellers can only buy credits from distributors; HalabTech is a plain reseller',
      direction='Chimera -> {GsmEasy | GsmServer | Unlock.eu} -> HalabTech', groups=['GRP-S-242'], r6='CONFIRMED (reseller only)', r7='CONFIRMED (reseller only)', tids=['W4-01', 'W4-02'], alt='', contra='', confirm='', reject=''),
    E(id='VEN-029', name='Ultimate Multi Tool (UMT) / NCK team', url='https://umt-pro.com', type='Original Developer', rel='HalabTech not on UMT distributor list (R6); Fast Unlocking is the team server',
      direction='UMT -> Fast Unlocking -> HalabTech (LIKELY)', groups=['GRP-S-244', 'GRP-S-104', 'GRP-S-052', 'GRP-S-314', 'GRP-S-313'], r6='CONFIRMED (absence)', r7='CONFIRMED (absence)', tids=['W4-07', 'V7-15'], alt='', contra='', confirm='', reject=''),
    E(id='VEN-013', name='Easy-Firmware team (EFT)', url='https://eftprodongle.com/packages', type='Original Developer', rel='HalabTech absent from EFT lists; official retail above HalabTech on 1Y/6M/3M',
      direction='EFT -> unnamed distributor -> HalabTech', groups=['GRP-S-240'], r6='CONFIRMED (absence)', r7='CONFIRMED (absence)', tids=['W4-06'], alt='', contra='', confirm='', reject=''),
    E(id='VEN-028', name='Furious Gold (FuriousTeam)', url='https://furiousgold.com', type='Original Developer', rel='HalabTech not listed; HalabTech credit $0.878 below all public offers',
      direction='Furious -> unnamed distributor -> HalabTech', groups=['GRP-S-248', 'GRP-S-279'], r6='CONFIRMED (absence)', r7='CONFIRMED (absence)', tids=['W4-08'], alt='', contra='', confirm='', reject=''),
    E(id='VEN-082', name='Dhru Cloud Pvt Ltd (Dhru Fusion)', url='https://dhru.com', type='Original Developer; Platform', rel="Platform of server.halabtech.com; HalabTech resells Dhru licences/add-ons under Dhru's names",
      direction='Dhru (or a Dhru distributor) -> HalabTech -> server builders', groups=['GRP-S-214'], r6='CONFIRMED (platform; resale)', r7='CONFIRMED (platform; resale); supply route UNKNOWN', tids=['W7-17', 'W4-21', 'W1-11'], alt='', contra='', confirm='', reject=''),
    E(id='VEN-083', name='Syriatel / MTN Syria (operators)', url='https://www.syriatel.sy/services/denominations-of-recharging-cards', type='Original issuer (telecom)',
      rel="HalabTech's Syriatel SKUs are the operator's official pre-tax denominations; recharge channel unidentified (manual/self-fulfilled fits)", direction='operator -> [unknown channel] -> HalabTech',
      groups=['GRP-S-080', 'GRP-S-081'], r6='UNKNOWN', r7='UNKNOWN (channel)', tids=['W7-01', 'W7-02'], alt='', contra='', confirm='', reject=''),
    E(id='VEN-084', name='Wondershare (Dr.Fone)', url='https://drfone.wondershare.com', type='Original Developer', rel='Dr.Fone licence names shared by >=12 servers; source unresolved',
      direction='unknown', groups=['GRP-S-227'], r6='-', r7='UNKNOWN', tids=['W7-16'], alt='', contra='', confirm='', reject=''),
    # --- platforms (not suppliers) ---
    E(id='PLT-001', name='Layout Team (layouteam.com)', url='https://layouteam.com', type='Platform (hosting / mail)', rel="HalabTech's SPF authorises Layout Team's server; api.store.halabtech.com resolves to it",
      direction='Layout Team -> HalabTech (hosting)', groups=['GRP-S-293'], r6='-', r7='CONFIRMED (hosting); not a supplier of GSM services', tids=['W1-02'], alt='', contra='', confirm='', reject=''),
    E(id='PLT-002', name='HTD (htdtech.dev)', url='https://htdtech.dev/', type='Platform (store SaaS); product resold by HalabTech', rel="store.halabtech.com runs on HTD CRM; HalabTech sells 'HTD Build Your Store' plans; ownership unproven",
      direction='HTD -> HalabTech', groups=['GRP-S-260'], r6='-', r7='CONFIRMED (platform); LIKELY (plan supply)', tids=['W1-03'], alt="'HTD' may be HalabTech's own brand.", contra='', confirm='', reject=''),
    E(id='PLT-003', name='JoudiSoft (Real Easy Store)', url='https://support.halabtech.com/', type='Platform (support.halabtech.com)', rel='Software licence for the support/downloads site',
      direction='JoudiSoft -> HalabTech (software)', groups=[], r6='CONFIRMED (VEN-015)', r7='CONFIRMED', tids=['W1-19'], alt='', contra='', confirm='', reject=''),
    E(id='PLT-004', name='Cloudflare / GoDaddy', url='https://rdap.org/domain/halabtech.com', type='Platform (DNS/CDN/registrar)', rel='Infrastructure only', direction='-',
      groups=[], r6='-', r7='CONFIRMED (infrastructure; not a supplier)', tids=['W1-01'], alt='', contra='', confirm='', reject=''),
    # --- downstream customers (selection; each with direct evidence) ---
    E(id='CUS-001', name='ReUnlocker (reunlocker.com)', url='https://reunlocker.com/resellerpricing/imei', type='Downstream Customer (API mirror)', rel='Mirrors 74.9% of IMEI and 81.5% of server names incl. test SKUs and memberships',
      direction='HalabTech -> ReUnlocker', groups=[], r6='(SUP-028)', r7='STRONG', tids=['W6-01', 'W6-16'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-002', name='MW Unlocker (mwunlocker.com, India)', url='https://www.mwunlocker.com/resellerpricing/imei', type='Downstream Customer (API mirror)', rel="85.5% of HalabTech IMEI names; sells 'HalabTech Point'",
      direction='HalabTech -> MW Unlocker', groups=[], r6='(SUP-028)', r7='STRONG', tids=['W6-02'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-003', name='GSM Tiger (gsmtiger.com)', url='https://gsmtiger.com/resellerpricing/server', type='Downstream Customer (API mirror)', rel='52.8% IMEI / 62.3% server names; memberships also via an intermediary with IDs #4562-#4571',
      direction='HalabTech -> GSM Tiger (direct and via an intermediary)', groups=[], r6='(SUP-028)', r7='STRONG', tids=['W6-03'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-004', name='univ gsm (univgsm.com, Ethiopia)', url='https://univgsm.com/resellerpricing/imei', type='Downstream Customer (API import)', rel="'TEST API IMEI' at x1.08; 29 SKUs at x1.0217; Moldova at x1.0143",
      direction='HalabTech -> univgsm', groups=[], r6='(SUP-028)', r7='STRONG', tids=['W6-04', 'V7-20'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-005', name='Saudi-GSM (saudi-gsm.com)', url='https://saudi-gsm.com/resellerpricing/server', type='Downstream Customer (API mirror)', rel="55.7% server names incl. Syrian/Turkish top-ups and 'TEST API CODE' at x1.1",
      direction='HalabTech -> Saudi-GSM', groups=[], r6='(SUP-009)', r7='STRONG', tids=['W6-05'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-006', name='HOS Unlocker (hos-unlocker.com, Egypt)', url='https://hos-unlocker.com/resellerpricing/server', type='Downstream Customer (dealer)', rel='Resells HalabTech products 2.8-12.5% below HalabTech list (dealer tier)',
      direction='HalabTech -> HOS', groups=[], r6='-', r7='STRONG', tids=['W7-05', 'V7-18'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-007', name='Eagle Unlocker / Ariqisoft / Fast Unlock', url='https://eagleunlocker.com/resellerpricing/server', type='Downstream Customers', rel='HalabTech price x1.05 / x1.035 / +$3.00 on digital goods',
      direction='HalabTech -> each', groups=[], r6='(SUP-028 eagleunlocker)', r7='LIKELY', tids=['W7-06', 'W7-07', 'W7-08'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-008', name='Best4unlock (best4unlock.us)', url='https://www.best4unlock.us/resellerpricing/imei', type='Reseller (peer); downstream for digital goods', rel="Sibling on Apple checks ('Prheck' typo); HalabTech-style digital names posted after HalabTech",
      direction='peer; HalabTech -> Best4unlock (digital goods)', groups=['GRP-I-009', 'GRP-S-237'], r6='UNKNOWN (SUP-016)', r7='LIKELY (peer / downstream for digital goods)', tids=['W6-13', 'W7-09', 'W2-15'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-009', name='GX Unlocker / unlockresellers / gsmlegion / tinunlock / imei247 / gsmalo', url='https://gxunlocker.com/resellerpricing/imei', type='Downstream Customers (probable)',
      rel="Reuse HalabTech names/typos ('Netowrk', 'NETOWRK', '( New User)') or price at fixed ratios of HalabTech", direction='HalabTech -> each', groups=[], r6='-', r7='LIKELY',
      tids=['W6-14', 'W6-17', 'W4-12', 'W3-04'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-010', name='Product resellers: WARD, MrUnlockers, GSMUnlockInfo, CleanUnlocker, Unlock-UA, DMUnlocker, Fix4GSM, IDUnlocker', url='https://wardserver.com/resellerpricing/server',
      type='Downstream Customers (HalabTech products only)', rel='Sell HalabTech memberships/credits; <=1.5% IMEI overlap', direction='HalabTech -> each', groups=['GRP-S-247'], r6='(SUP-028)', r7='STRONG',
      tids=['W6-15'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-011', name='SosoGSM (sosogsm.net) and "menet"', url='https://sosogsm.net', type='Downstream Customer (probable, AI bot product)',
      rel='chatsosogsm/chatmenet.halabtech.com certificates fit buyers of HalabTech\'s "AI Bot For Gsm Site"; SosoGSM is also a TONI PRO TOOL reseller', direction='HalabTech -> SosoGSM (inferred)',
      groups=['GRP-S-136', 'GRP-S-161'], r6='-', r7='LIKELY', tids=['V7-22', 'W1-06'], alt='Partner rather than buyer.', contra='', confirm='', reject=''),
    E(id='CUS-012', name='Downstream servers carrying HalabTech T-Mobile/Source labels (globaldsm, dzunlocker, gsmsewanepal, cheapunlocker, ...)', url='https://globaldsm.net',
      type='Downstream Customers (probable)', rel="Keep HalabTech's private labels ('[Premium ]' typo, 'Source #2', 'Source #3')", direction='HalabTech -> each', groups=['GRP-I-008', 'GRP-I-023', 'GRP-I-017'],
      r6='(B-10, B-19)', r7='LIKELY', tids=['W2-06', 'W2-15'], alt='', contra='', confirm='', reject=''),
    E(id='CUS-013', name='HalabTech World Agents 2019 (gsmfastest, mygsm24, imeipk, ...)', url='https://web.archive.org/web/20190718171635/https://support.halabtech.com/index.php?a=pages&b=world-agents',
      type='Downstream agents (historical)', rel='2019 baseline of the agent network (support accounts)', direction='HalabTech -> agents', groups=[], r6='CONFIRMED (SUP-029, current)', r7='CONFIRMED (2019 baseline)',
      tids=['W1-15'], alt='', contra='', confirm='', reject=''),
]

# --------------------------------------------------------------------------------------------------------------
# 5. Suspected supply chains (curated; every link graded). Vendor-listing chains are generated automatically.
#    Fields: id, dev, md, api, reseller, ht ('HalabTech' role), cust, groups, link_conf (list of (link, conf)),
#    conf (weakest), etype, tids, direction, alt, contra, confirm, reject
# --------------------------------------------------------------------------------------------------------------
C = lambda **k: k
CHAINS = [
    C(id='CH-S01', dev='SigmaKey team', md='GsmServer (exclusive distributor)', api='GsmServer panel / sub-reseller (activations)', ht='Reseller', cust='HalabTech clients; downstream mirrors',
      groups=['GRP-S-072', 'GRP-S-252'], links=[('Sigma -> GsmServer', 'CONFIRMED'), ('GsmServer -> HalabTech', 'STRONG')], conf='STRONG', etype='vendor page; price fingerprint; Wayback',
      tids=['W4-04', 'V7-27', 'W4-05', 'W1-07', 'V7-12'], direction='Vendor rule (exclusive distributor) fixes direction', alt='Activations via a GsmServer sub-reseller (GsmEasy near-match).',
      contra='GsmServer retail for activations above HalabTech; HalabTech licence prices are 6-13% below RRP although Sigma allows max 5% discount (V7-27).', confirm='GsmServer/HalabTech naming the account.', reject='Sigma naming another distributor.'),
    C(id='CH-S02', dev='ChimeraTool', md='GsmEasy | GsmServer | Unlock.eu (distributor tier, $0.092/credit)', api='-', ht='Reseller (plain)', cust='HalabTech clients',
      groups=['GRP-S-242'], links=[('Chimera -> distributors', 'CONFIRMED'), ('one distributor -> HalabTech', 'STRONG'), ('which distributor', 'UNKNOWN')], conf='STRONG',
      etype='vendor page; price fingerprint', tids=['W4-01', 'W4-02', 'W4-03', 'V7-13'], direction='Vendor rule: resellers buy only from distributors',
      alt='', contra='Chimera text names two distributors; page shows three cards (CL-021).', confirm='Distributor naming HalabTech.', reject='Chimera listing HalabTech as distributor.'),
    C(id='CH-S03', dev='Hunter Unlocker / Q-Unlocker', md='-', api='-', ht='WorldWide Distributor (1 of 3)', cust='HalabTech clients; resellers',
      groups=['GRP-S-264', 'GRP-S-182'], links=[('vendor -> HalabTech', 'STRONG')], conf='STRONG', etype='vendor page', tids=['V7-04', 'V7-05'],
      direction='Vendor rule: no direct sales to agents', alt='', contra='', confirm='Vendor API naming HalabTech.', reject=''),
    C(id='CH-S04', dev='XTP - Xiaomi Tool Pro', md='-', api='-', ht='"Official Main Seller"', cust='HalabTech clients', groups=['GRP-S-189'],
      links=[('XTP -> HalabTech', 'STRONG')], conf='STRONG', etype='vendor page', tids=[], direction='Vendor statement', alt='', contra='', confirm='', reject=''),
    C(id='CH-S05', dev='Various (Sigma packs, Octoplus credits, Boot-Loader 2.0, GB Key)', md='GsmServer', api='-', ht='Reseller (historical group "GsmServer Products")',
      cust='HalabTech clients 2020-2024; group label still copied by UnlocksPro, gsmlegion', groups=[], links=[('GsmServer -> HalabTech (2020-2024)', 'STRONG')], conf='STRONG',
      etype='Wayback; catalog genealogy', tids=['W1-07', 'V7-12', 'W4-03', 'W4-12', 'V7-11'], direction="HalabTech's own group label names GsmServer",
      alt="Label could denote GsmServer-branded products rather than purchase route.", contra='Group absent from the 2026 catalog.', confirm='Dated purchase record or GsmServer statement.', reject=''),
    C(id='CH-S06', dev='UMT / NCK / Avengers team', md='Fast Unlocking (team activation server)', api='Fast Unlocking (server APIs)', ht='Reseller', cust='HalabTech clients; HOS (UMT WebOwner SKU)',
      groups=['GRP-S-244', 'GRP-S-104', 'GRP-S-052', 'GRP-S-314', 'GRP-S-313'], links=[('UMT -> Fast Unlocking', 'CONFIRMED'), ('Fast Unlocking -> HalabTech', 'LIKELY')], conf='LIKELY',
      etype='price fingerprint; vendor page', tids=['W4-07', 'V7-15'], direction='Price position only', alt='Another UMT distributor with non-public API prices.', contra='',
      confirm='Fast Unlocking API price = HalabTech cost for >=3 SKUs.', reject='HalabTech prices below Fast Unlocking reseller prices.'),
    C(id='CH-S07', dev='Cerberus Tool', md='-', api='Cerberus seller dashboard (DHRU-compatible API)', ht='Special Distributor', cust='HalabTech clients', groups=['GRP-S-012'],
      links=[('Cerberus -> HalabTech (authorisation)', 'CONFIRMED'), ('via vendor API', 'LIKELY')], conf='LIKELY', etype='vendor page; catalog change (rename sync)',
      tids=['W5-69', 'W5-72', 'V7-02', 'V7-17'], direction='Vendor lists HalabTech; names synced to vendor products', alt='Manual rename.', contra='Prices not one markup over vendor public prices.',
      confirm='Vendor API names/IDs = HalabTech SKU strings.', reject='HalabTech SKUs matching another distributor catalogue.'),
    C(id='CH-S08', dev='Alseery Unlocker; F-KEY TOOL', md='-', api='GSM Nigeria (candidate)', ht='Reseller', cust='HalabTech clients', groups=['GRP-S-262', 'GRP-S-096'],
      links=[('GSM Nigeria -> HalabTech', 'LIKELY')], conf='LIKELY', etype='price fingerprint', tids=['W6-09', 'V7-19'], direction='GSM Nigeria price = HalabTech implied cost (exact, 4 SKUs)',
      alt='Common upstream at 0.68/1.08.', contra='GSM Nigeria resells HalabTech credits and a HalabTech group typo (downstream for those).', confirm='Synchronous price moves.', reject='Older HalabTech cost history.'),
    C(id='CH-S09', dev='Orange Moldova (carrier unlock)', md='-', api='GSMFATHER (IDs 1351#/1352#) or its upstream', ht='Reseller', cust='HalabTech clients; univgsm (x1.0143)',
      groups=['GRP-I-028'], links=[('GSMFATHER -> HalabTech', 'LIKELY')], conf='LIKELY', etype='catalog genealogy (embedded IDs)', tids=['W6-11', 'V7-21', 'V7-20'],
      direction='Upstream IDs embedded in HalabTech names', alt="IDs may belong to GSMFATHER's own upstream.", contra='GSMFATHER page now 404.', confirm='GSMFATHER record of IDs 1351/1352.', reject='Older carrier of 1351#.'),
    C(id='CH-S10', dev='GsmAuth.com', md='-', api='GsmDone.com (vendor-declared Dhru Web API partner)', ht='Reseller', cust='HalabTech clients', groups=['GRP-S-109'],
      links=[('GsmDone -> HalabTech', 'LIKELY')], conf='LIKELY', etype='vendor page', tids=['W5-76'], direction='Vendor declares GsmDone as the API route for other sites', alt='GsmAuth direct.', contra='HalabTech SKU at $0.',
      confirm='GsmDone catalogue match.', reject=''),
    C(id='CH-S11', dev='SETool team', md='GsmEasy (sole distributor named)', api='-', ht='Reseller (not listed)', cust='HalabTech clients', groups=['GRP-S-233'],
      links=[('SETool -> GsmEasy', 'CONFIRMED'), ('GsmEasy -> HalabTech', 'LIKELY')], conf='LIKELY', etype='vendor page', tids=['W5-77'], direction='Only distributor named', alt='GsmEasy reseller in between.', contra='Old support page.',
      confirm='Current SETool distributor list; price parity.', reject=''),
    C(id='CH-S12', dev='CF Tools (cftoolsid.com)', md='AppleUnlockers (single Main Distributor)', api='-', ht='Worldwide Reseller', cust='HalabTech clients', groups=['GRP-S-263', 'GRP-S-319'],
      links=[('CF Tools -> AppleUnlockers', 'CONFIRMED'), ('AppleUnlockers -> HalabTech', 'LIKELY')], conf='LIKELY', etype='distributor directory', tids=['W5-75', 'W5-21'], direction='Vendor tiering',
      alt='Direct reseller account.', contra='', confirm='Vendor statement.', reject=''),
    C(id='CH-S13', dev='Tira / TheMagicTool / GuerraTool / Panda', md='ADY Unlocker (sole distributor / only worldwide reseller)', api='-', ht='Reseller (Tira) / not listed (Magic, Guerra)',
      cust='HalabTech clients', groups=['GRP-S-203', 'GRP-S-226', 'GRP-S-300', 'GRP-S-306'], links=[('vendor -> ADY', 'CONFIRMED'), ('ADY -> HalabTech', 'LIKELY')], conf='LIKELY',
      etype='distributor directory', tids=['W5-78', 'W5-05', 'W5-88'], direction='Vendor tiering', alt='Direct accounts.', contra='ADY also consumes HalabTech catalog strings (W4-18).',
      confirm="ADY strings/prices = HalabTech's.", reject=''),
    C(id='CH-S14', dev='Easy-Firmware team (EFT)', md='Easy Team / another EFT distributor', api='-', ht='Reseller (not listed)', cust='HalabTech clients', groups=['GRP-S-240'],
      links=[('EFT -> distributors', 'CONFIRMED'), ('a distributor -> HalabTech', 'LIKELY'), ('which', 'UNKNOWN')], conf='LIKELY', etype='vendor page; price fingerprint (no match)',
      tids=['W4-06', 'V7-04'], direction='HalabTech absent from EFT lists', alt='', contra='No candidate price fits >=2 SKUs.', confirm='', reject=''),
    C(id='CH-S15', dev='Furious Gold', md='An unnamed FG distributor', api='-', ht='Reseller (not listed)', cust='HalabTech clients', groups=['GRP-S-248', 'GRP-S-279'],
      links=[('FG -> distributors', 'CONFIRMED'), ('a distributor -> HalabTech', 'LIKELY'), ('which', 'UNKNOWN')], conf='LIKELY', etype='vendor page; price fingerprint (undercuts all)',
      tids=['W4-08'], direction='HalabTech absent from FG list', alt='', contra='', confirm='', reject=''),
    C(id='CH-S16', dev='Octoplus team', md='-', api='-', ht='Official reseller', cust='HalabTech clients', groups=['GRP-S-170', 'GRP-S-206', 'GRP-S-215', 'GRP-S-251', 'GRP-S-288', 'GRP-S-289', 'GRP-S-290', 'GRP-S-291'],
      links=[('Octoplus -> HalabTech (authorisation)', 'CONFIRMED'), ('direct supply', 'LIKELY')], conf='LIKELY', etype='vendor page; price fingerprint', tids=['W5-71', 'W4-15'],
      direction='Official reseller; $0.10 shared reseller cost', alt='GsmServer (historical Octoplus credits in GsmServer Products).', contra='', confirm='', reject=''),
    C(id='CH-S17', dev='Hydra Tool team', md='-', api='-', ht='Dongle/License Agent', cust='HalabTech clients', groups=['GRP-S-059', 'GRP-S-193', 'GRP-S-278'],
      links=[('Hydra -> HalabTech (agent status)', 'CONFIRMED'), ('direct supply', 'LIKELY')], conf='LIKELY', etype='vendor page; price fingerprint', tids=['W4-10', 'V7-16'],
      direction='Agent status', alt='', contra='Vendor retail leg not re-confirmed.', confirm='', reject=''),
    C(id='CH-D01', dev='T-Mobile USA policy unlock (carrier)', md='?', api='Code-GSM | NNNN#-B upstream (3277#-3281#) | HalabTech origin', ht='Reseller or origin', cust='TinUnlock, imei247, gsmalo, reunlocker, khulnaunlock',
      groups=['GRP-I-018'], links=[('Code-GSM -> HalabTech', 'DISPUTED'), ('common upstream -> both', 'UNKNOWN')], conf='DISPUTED', etype='timing; price structure; catalog genealogy',
      tids=['V7-08', 'W2-08', 'W3-01', 'W3-02', 'W3-08', 'W6-12', 'W3-04'], direction='HalabTech posted first (2 Mar 2026); price structure fits Code-GSM->HalabTech or common upstream',
      alt='Sibling of a common upstream (most parsimonious).', contra='HalabTech = Code-GSM + whole dollars (identical cents).', confirm='Dated Code-GSM listing before 2 Mar 2026; Code-GSM naming HalabTech.', reject='Code-GSM first appearance after HalabTech for every tier.'),
    C(id='CH-D02', dev='Various (Signal Labs, JDM, Reseller Flex, MDM)', md='-', api='UnlocksPro (R6 hypothesis)', ht='Reseller', cust='-', groups=['GRP-I-000', 'GRP-I-048', 'GRP-I-054', 'GRP-I-012', 'GRP-I-013'],
      links=[('UnlocksPro -> HalabTech', 'DISPUTED')], conf='DISPUTED', etype='catalog genealogy; Wayback', tids=['W3-09', 'W3-10', 'W3-11', 'W6-06', 'W6-07', 'V7-11'],
      direction='Evidence reverses direction: HalabTech -> UnlocksPro', alt='Reciprocal route for a few items.', contra='', confirm='', reject='(already contradicted)'),
    C(id='CH-U01', dev='T-Mobile USA (Premium iPhone unlock)', md='?', api='Unnamed source at $115/$125', ht='Reseller (markup 6.0% -> 4.5%)', cust='globaldsm, dzunlocker, ethio-gsm, ... (10 servers)',
      groups=['GRP-I-008'], links=[('unnamed -> HalabTech', 'UNKNOWN')], conf='UNKNOWN', etype='price fingerprint', tids=['V7-01', 'W2-04', 'W2-05', 'W2-06'], direction='Fingerprint only',
      alt='', contra='', confirm='Public $115/$125 price at a server.', reject=''),
    C(id='CH-U02', dev='Apple GSX data', md='?', api="Unnamed 2020 GSX upstream (IDs #225/#33225/32596)", ht='Reseller', cust='mwunlocker, univgsm, gs-server (variants)', groups=['GRP-I-040'],
      links=[('unnamed -> HalabTech', 'UNKNOWN')], conf='UNKNOWN', etype='catalog genealogy (embedded IDs)', tids=['W2-10', 'W2-11', 'W1-08'], direction='IDs embedded since 2020', alt='', contra='', confirm='', reject=''),
    C(id='CH-U03', dev='Signal Labs Technology', md='?', api='Unnamed API supplier ($17.95/$21.95/$4.50/$5.53)', ht='Reseller (x1.15-1.25)', cust='-', groups=['GRP-I-000'],
      links=[('unnamed -> HalabTech', 'UNKNOWN')], conf='UNKNOWN', etype='price fingerprint', tids=['W3-13'], direction='Computed prices', alt='', contra='', confirm='Priced listing at those costs.', reject=''),
    C(id='CH-U04', dev='Samsung / Tecno-Infinix-Itel / Xiaomi IMEI services', md='?', api="Unnamed numbered sources (Source #1-#4, 'Server Direct')", ht='Router across sources',
      cust='Code-GSM (Mi Account), gsmsewanepal, cheapunlocker, ...', groups=['GRP-I-017', 'GRP-I-023', 'GRP-I-025', 'GRP-I-036', 'GRP-I-021'], links=[('sources -> HalabTech', 'UNKNOWN (identities)')],
      conf='UNKNOWN', etype='Telegram; catalog labels', tids=['W2-01', 'W2-02', 'W2-13', 'V7-14', 'V7-10'], direction='HalabTech labels', alt='', contra='', confirm='', reject=''),
    C(id='CH-U05', dev='Samsung CPID / EDL / JDM repair', md='?', api='Unnamed CPID/EDL operator (nevutek, imeishop, serverunlocker, GSM Nigeria "Direct Distributor" leads)', ht='Reseller',
      cust='univgsm (x1.0217), UnlocksPro, GX Unlocker', groups=['GRP-I-047', 'GRP-I-048', 'GRP-I-050', 'GRP-I-051', 'GRP-I-056'], links=[('operator -> HalabTech', 'UNKNOWN')], conf='UNKNOWN',
      etype='Telegram timing; catalog genealogy', tids=['W2-16', 'V7-19', 'V7-20', 'W3-10'], direction='-', alt='', contra='', confirm='', reject=''),
    C(id='CH-U06', dev='iRemove Software (FMI OFF iPad/iWatch)', md='?', api='iRemove partner | GSM Nigeria -> Code-GSM cluster', ht='Reseller', cust='-', groups=['GRP-I-019', 'GRP-I-020'],
      links=[('partner -> HalabTech', 'UNKNOWN')], conf='UNKNOWN', etype='price comparison', tids=['W2-12', 'W6-10', 'W6-08'], direction='-', alt='', contra='', confirm='', reject=''),
    C(id='CH-U07', dev='Garena / Krafton / Google / Apple / Sony (digital goods)', md='?', api="Unnamed voucher wholesalers; TRY face-value-linked e-pin API; '(AUTO API)' PUBG top-up", ht='Reseller; own code stock',
      cust='HOS, Eagle Unlocker, Ariqisoft, Fast Unlock, Best4unlock, ~25 servers', groups=['GRP-S-230', 'GRP-S-237', 'GRP-S-238', 'GRP-S-220', 'GRP-S-221', 'GRP-S-204', 'GRP-S-256', 'GRP-S-257'],
      links=[('wholesaler -> HalabTech', 'UNKNOWN')], conf='UNKNOWN', etype='price fingerprint; Telegram', tids=['W7-04', 'W7-11', 'W7-13', 'W7-14', 'W7-10'], direction='-', alt='', contra='', confirm='', reject=''),
    C(id='CH-U08', dev='Syriatel / MTN (operators)', md='-', api='Unidentified recharge channel (manual / own wallets fits)', ht='Reseller', cust='Saudi-GSM and other mirrors', groups=['GRP-S-080', 'GRP-S-081'],
      links=[('channel -> HalabTech', 'UNKNOWN')], conf='UNKNOWN', etype='vendor page; Telegram', tids=['W7-01', 'W7-02'], direction='-', alt='', contra='', confirm='', reject=''),
]

# --------------------------------------------------------------------------------------------------------------
# 6. Unresolved cases (ranked in the engine by SKUs; curated text here). GAP ids continue R6 numbering.
# --------------------------------------------------------------------------------------------------------------
U = lambda **k: k
UNRESOLVED = [
    U(id='GAP-011', q='Which Chimera distributor (GsmEasy, GsmServer or Unlock.eu) supplies HalabTech?', groups=['GRP-S-242'], best='One of three distributors at $0.092/credit (STRONG that it is a distributor)',
      conf='STRONG (route) / UNKNOWN (which)', missing='Any document naming the specific distributor', confirm='A distributor naming HalabTech as its reseller; Chimera reseller-page metadata',
      reject='-', method='Daily price-series of the three distributors vs HalabTech Chimera SKUs (synchronous change test)', prio='Medium', status='Narrowed (3 candidates, none excluded)'),
    U(id='GAP-012', q='Which EFT channel supplies HalabTech?', groups=['GRP-S-240'], best='Easy Team or another EFT distributor', conf='LIKELY (route) / UNKNOWN (which)',
      missing='Price match; listing', confirm='EFT channel price sheet = HalabTech cost', reject='-', method='Collect EFT distributor reseller price sheets (public)', prio='Medium', status='Open'),
    U(id='GAP-013', q='Which UMT/NCK/Avengers and Furious Gold distributors supply HalabTech?', groups=['GRP-S-244', 'GRP-S-104', 'GRP-S-052', 'GRP-S-314', 'GRP-S-313', 'GRP-S-248', 'GRP-S-279'],
      best='Fast Unlocking (UMT/NCK/AVB, LIKELY); FG unnamed', conf='LIKELY', missing='Fast Unlocking API prices; FG distributor below $0.80', confirm='API price = HalabTech cost',
      reject='HalabTech below Fast Unlocking reseller prices', method='Public reseller price pages of Fast Unlocking; FG distributors', prio='Medium', status='Narrowed (UMT/NCK/AVB)'),
    U(id='GAP-014', q='T-Mobile Clean & Paid Off: Code-GSM, a common upstream (IDs 3277#-3281#) or HalabTech origin?', groups=['GRP-I-018'], best='Common upstream (most parsimonious); Code-GSM->HalabTech not excluded',
      conf='DISPUTED', missing='Dated Code-GSM listing before 2 Mar 2026; identity of the 3277#-3281# server', confirm='Code-GSM listing pre-2 Mar 2026 (Code-GSM upstream) or 3277# server = both sources',
      reject='Code-GSM appearing only after HalabTech everywhere', method='Wayback/Telegram first-appearance per tier; search native IDs 3277-3281', prio='High', status='Reframed (CL-013 resolved: stale cache)'),
    U(id='GAP-015', q='Direction HalabTech <-> UnlocksPro', groups=['GRP-I-000', 'GRP-I-048', 'GRP-I-054', 'GRP-I-013'], best='HalabTech -> UnlocksPro (downstream)', conf='STRONG (server) / LIKELY (IMEI)',
      missing='-', confirm='-', reject='HalabTech names carrying UnlocksPro IDs', method='-', prio='Low', status='Resolved (downstream)'),
    U(id='GAP-016', q='Is HalabTech an iRemove partner, or does it buy FMI OFF via another partner?', groups=['GRP-I-019', 'GRP-I-020'], best='Unknown; GSM Nigeria -> Code-GSM (+$2) cluster is a sibling',
      conf='UNKNOWN', missing='Partner list; fixed price offsets', confirm='Constant offset to one seller across models', reject='-', method='Model-by-model price ratio test across >=5 sellers on one timestamp', prio='High', status='Open'),
    U(id='GAP-018', q='Long-tail tool vendors without a checked list', groups=[], best='205 groups recorded: 80 listed, 18 absent, 107 no list/unreachable', conf='-',
      missing='Lists for 107 groups (64 no public/rendered list, 32 vendor not found, 11 unreachable)', confirm='-', reject='-', method='Wayback copies of reseller pages; vendor Telegram channels', prio='Medium', status='Largely done'),
    U(id='GAP-019', q='Gift-card / game / telecom / AI-subscription suppliers', groups=['GRP-S-230', 'GRP-S-237', 'GRP-S-238', 'GRP-S-220', 'GRP-S-221', 'GRP-S-204', 'GRP-S-256', 'GRP-S-257', 'GRP-S-080', 'GRP-S-081', 'GRP-S-172'],
      best='Own stock / manual / face-value-linked TRY API; no wholesaler named', conf='UNKNOWN', missing='Wholesaler price tables at matching timestamps',
      confirm='Implied costs ($0.90/60 UC; 0.021174 USD/TL; 0.278 USD/AED) matching a wholesaler', reject='-', method='Same-hour price capture of Turkpin/Oyuneks/FazerCards/Kinguin-type B2B public tables', prio='Medium', status='Narrowed'),
    U(id='GAP-020', q='Markup fingerprinting (3-decimal prices)', groups=[], best='232 computed SKUs / 73 groups with shared multiplier; matches: Alseery/F-KEY (GSM Nigeria), Chimera ($0.092), Sigma panel, Octoplus ($0.10)',
      conf='-', missing='Matches for T-Mobile Premium ($115/$125), Signal Labs, Deep Unlocker ($0.55/$55), TSM ($0.75), TFM ($0.90)', confirm='-', reject='-',
      method='Extend to more candidate catalogs at matching timestamps', prio='High', status='Done (method); partial matches'),
    U(id='GAP-021', q='Why did the catalog shrink (2022: 385 groups / 1,705 SKUs -> 2026: 383 / 1,455)?', groups=[], best='Platform history 2019-2020 reconstructed; no diff of dropped lines yet', conf='-',
      missing='2023-2025 catalog captures', confirm='-', reject='-', method='Wayback 2023/2025 resellerpricing captures', prio='Low', status='Open'),
    U(id='GAP-022', q='Legal entity / beneficial owner of HalabTech', groups=[], best='Registrant private; hosting by Layout Team; Syria/Turkey contacts', conf='UNKNOWN', missing='Registry records',
      confirm='-', reject='-', method='Public company registries (TR/AE) - lawful lookups only', prio='Low', status='Open'),
    U(id='GAP-023', q='Who sells the T-Mobile Premium unlocks at $115.00 / $125.00?', groups=['GRP-I-008'], best='Unnamed source (fingerprint CONFIRMED)', conf='UNKNOWN',
      missing='A public price at $115/$125', confirm='Server listing both at $115/$125 (or tracking HalabTech changes)', reject='-', method='Snapshot candidate T-Mobile premium sellers hourly; watch for HalabTech re-pricing events', prio='High', status='New'),
    U(id='GAP-024', q='GSM Nigeria: upstream for Alseery/F-KEY (and CPID "Direct Distributor") or HalabTech dealer?', groups=['GRP-S-262', 'GRP-S-096', 'GRP-I-050', 'GRP-I-051', 'GRP-I-056'],
      best='Two-way relationship; exact implied-cost matches favour GSM Nigeria -> HalabTech for Alseery/F-KEY', conf='LIKELY', missing='Direction evidence (dates, IDs)',
      confirm='GSM Nigeria IDs in HalabTech names; synchronous price moves', reject='HalabTech price history predating GSM Nigeria', method='Paired daily price series; Wayback first appearance of shared typos', prio='High', status='New'),
    U(id='GAP-025', q="Origin of GSX IDs '#225', '#33225', '32596' (since 2020)", groups=['GRP-I-040'], best='Unnamed 2020 upstream', conf='UNKNOWN', missing='Server with native IDs in that range',
      confirm='Native service IDs 225/33225/32596 on one server', reject='-', method='Search 2020 Wayback captures of GSX-check servers', prio='Medium', status='New'),
    U(id='GAP-026', q='Signal Labs supplier (implied costs $17.95/$21.95/$4.50/$5.53)', groups=['GRP-I-000'], best='Unnamed API supplier', conf='UNKNOWN', missing='Priced listings',
      confirm='Listing at those costs', reject='-', method="Price capture of servers carrying '4389# Signal Labs ...' (beeunlock) and UnlocksPro block", prio='Medium', status='New'),
    U(id='GAP-027', q='Identities of numbered IMEI sources (Samsung FRP Source #1-#4, MDM Source #2/#3, Mi Account routes)', groups=['GRP-I-017', 'GRP-I-023', 'GRP-I-025', 'GRP-I-036', 'GRP-I-021'],
      best='GsmUnlockingStore for the Apr-2026 Samsung FRP LEVEL 5 batch (LIKELY); others unnamed', conf='UNKNOWN', missing='Name or ID artefacts',
      confirm="Source-specific IDs/labels in HalabTech names; same-minute outages", reject='-', method="Correlate HalabTech 'Service Active/Inactive' bot posts with candidates' public status posts", prio='High', status='Open (GAP-001 successor)'),
    U(id='GAP-028', q='Samsung CPID / EDL / JDM operators (61 SKUs)', groups=['GRP-I-047', 'GRP-I-048', 'GRP-I-050', 'GRP-I-051', 'GRP-I-056'], best='Unnamed operator; leads nevutek, imeishop, serverunlocker, GSM Nigeria',
      conf='UNKNOWN', missing='Price or ID match', confirm='Operator prices = HalabTech cost', reject='-', method='Same-day price capture of CPID operators', prio='High', status='New'),
    U(id='GAP-029', q='Top-tier vendor relationships: API or manual fulfilment? (Cerberus, Pixel Pro, Eagle FRP, TMT, NEXTG, HXRU, UST, MobileProTool, Apizu, CheckerTR)', groups=['GRP-S-012', 'GRP-S-068', 'GRP-S-016', 'GRP-S-149', 'GRP-S-202', 'GRP-S-070', 'GRP-S-098', 'GRP-S-029', 'GRP-S-018', 'GRP-S-069', 'GRP-S-146'],
      best='Vendor direct (LIKELY); Cerberus API sync observed', conf='LIKELY', missing='SKU-name/ID sync evidence per vendor', confirm='Renames tracking vendor changes within minutes', reject='SKU parity with another distributor',
      method='Twice-daily catalog snapshots to catch name syncs', prio='Medium', status='New'),
    U(id='GAP-030', q="Moldova NNNN# origin: GSMFATHER or its upstream?", groups=['GRP-I-028'], best='GSMFATHER (LIKELY)', conf='LIKELY', missing='Live GSMFATHER record (page now 404)',
      confirm='GSMFATHER announcement of IDs 1351/1352', reject='Older carrier', method='GSMFATHER Telegram channel search', prio='Low', status='New'),
    U(id='GAP-031', q='HalabTech dealer-tier schedule (Reseller / Big Reseller / Web Owner discounts)', groups=[], best='Dealers observed 2.8-12.5% below list (HOS)', conf='-',
      missing='Published tier table', confirm='-', reject='-', method='Archived DISTRIBUTOR page and Telegram tier posts', prio='High', status='New (calibration for all price tests)'),
    U(id='GAP-032', q='SosoGSM / "menet": buyers of HalabTech AI bot, or partners? Is All Unlocker a HalabTech brand?', groups=['GRP-S-136', 'GRP-S-161'], best='Buyers (LIKELY)',
      conf='LIKELY', missing='Widget embed on sosogsm.net', confirm='SosoGSM widget posting to chatsosogsm.halabtech.com', reject='-', method='Public HTML of sosogsm.net; global-unlocker-pro.com distributor card', prio='Low', status='New'),
    U(id='GAP-033', q='HTD ownership (htdtech.dev) - HalabTech brand or third-party SaaS?', groups=['GRP-S-260'], best='Unproven', conf='UNKNOWN', missing='Ownership statement',
      confirm='HTD site naming HalabTech', reject='HTD naming an unrelated owner', method='htdtech.dev public pages; Telegram t.me/HTDtechdev', prio='Low', status='New'),
]

# --------------------------------------------------------------------------------------------------------------
# 7. Confidence Change Log (CL-022+): relationship/group/entity level + Phase-5 finding level
# --------------------------------------------------------------------------------------------------------------
L = lambda **k: k
CHANGES = [
    L(obj='REL-097 / SUP-014 Code-GSM -> HalabTech (T-Mobile Clean & Paid Off; GRP-I-018)', level='Relationship + group', before='LIKELY', after='DISPUTED',
      why="HalabTech's 2 Mar 2026 batch is the earliest dated appearance (GSM-Forum dates are MM-DD-YYYY); a third source carries the names under IDs 3277#-3281#; Code-GSM buys T-Mobile from 'supplier#2'. Price structure (identical cents) still fits Code-GSM->HalabTech or a common upstream.",
      tids=['V7-08', 'W2-08', 'W6-12', 'W3-08', 'W3-01']),
    L(obj='CL-013 Code-GSM listing vs detail price conflict', level='Conflict', before='DISPUTED', after='Resolved',
      why='R6 listing figures came from a stale cached copy; same-day listing = rounded detail prices.', tids=['W3-02', 'W3-01', 'W6-08']),
    L(obj='SUP-014 Code-GSM (role)', level='Entity', before='LIKELY (candidate upstream)', after='STRONG downstream (Mi Account, memberships); DISPUTED upstream (T-Mobile)',
      why="Code-GSM carries HalabTech's internal routing label 'Source2 #Cheaper' and malformed braces, and resells HalabTech memberships.", tids=['V7-10', 'W2-09', 'W3-06']),
    L(obj='REL-098 / SUP-015 UnlocksPro -> HalabTech', level='Relationship', before='LIKELY (direction unproven)', after='DISPUTED (direction reversed); HalabTech -> UnlocksPro STRONG',
      why='UnlocksPro resells HalabTech-proprietary products in contiguous import blocks and copied HalabTech IMEI names since 2023; its #NNNNN ids are its own and never appear in HalabTech names.',
      tids=['W3-09', 'W3-10', 'W3-11', 'W6-06', 'W6-07', 'V7-11']),
    L(obj='GRP-I-000 Signal Labs Technology Service', level='Group', before='LIKELY (UnlocksPro)', after='UNKNOWN', why='Basis (UnlocksPro as upstream) withdrawn; implied costs point to an unnamed API supplier.', tids=['W3-13', 'W3-11']),
    L(obj='GRP-I-013 Xiaomi Checker', level='Group', before='LIKELY (UnlocksPro)', after='UNKNOWN', why='Basis (UnlocksPro as upstream) withdrawn.', tids=['W3-10', 'W6-06']),
    L(obj='GRP-I-048 [NEW JDM V4 V5] SAMSUNG Repair', level='Group', before='LIKELY (UnlocksPro)', after='UNKNOWN', why="UnlocksPro copied HalabTech's 'Netowrk' names by 2024 (downstream).", tids=['W3-10']),
    L(obj='GRP-I-054 USA Reseller Flex', level='Group', before='LIKELY (UnlocksPro)', after='UNKNOWN', why="UnlocksPro used HalabTech's group by 2023 (downstream).", tids=['W3-10']),
    L(obj='REL-028 GsmServer -> HalabTech ("GsmServer Products")', level='Relationship (historical)', before='LIKELY (2022-2024)', after='STRONG (2020-2024)',
      why="HalabTech's own catalog labelled the group 'GsmServer Products' from at least June 2020 to 2024, containing Sigma packs (GsmServer = Sigma exclusive distributor) and Octoplus credits; confirmed by two tools.",
      tids=['W1-07', 'V7-12', 'W4-03']),
    L(obj='SUP-017 Fast Unlocking', level='Entity', before='UNKNOWN', after='LIKELY (UMT/NCK/Avengers source)', why="Only UMT/NCK distributor priced at or just below HalabTech; it is the team's activation server offering API support to other servers.",
      tids=['W4-07', 'V7-15']),
    L(obj='GRP-S-012 Cerberus Tool Pro', level='Group', before='UNKNOWN (not checked)', after='LIKELY (vendor API)', why="Vendor lists HalabTech first as 'Special Distributor' (2 tools) and offers a DHRU-compatible seller API; SKU rename fits API name-sync.",
      tids=['W5-69', 'V7-17', 'W5-72', 'V7-02']),
    L(obj='72 never-checked groups whose developer lists HalabTech (W5 LISTED)', level='Group (bulk)', before='UNKNOWN (not checked)', after='LIKELY (vendor direct, authorised channel)',
      why='Same R6 rule: official listing = authorised channel (CONFIRMED status), fulfilment route LIKELY.', tids=['W5-01']),
    L(obj='8 Octoplus groups', level='Group (bulk)', before='UNKNOWN (not mapped)', after='LIKELY (vendor direct)', why='Vendor already listed HalabTech in R6 (A1-10) but the groups were not linked; $0.10 shared reseller cost.', tids=['W5-71', 'W4-15']),
    L(obj='Groups whose developer omits HalabTech but names its channel (W5 ABSENT, 15 of 18)', level='Group (bulk)', before='UNKNOWN (not checked)', after="LIKELY (via vendor's listed channel)",
      why="Same R6 rule as REL-086..093; 3 stay UNKNOWN because the vendor also sells direct/API tiers (Roby, Easy Auth, Mysterio).", tids=['W5-77', 'W5-78', 'W5-80']),
    L(obj='GRP-S-262 Alseery Unlocker; GRP-S-096 F-KEY TOOL', level='Group', before='UNKNOWN', after='LIKELY (GSM Nigeria)', why="GSM Nigeria's prices equal HalabTech's implied costs exactly on 4 SKUs (two tools).",
      tids=['W6-09', 'V7-19']),
    L(obj='GRP-I-028 Moldova Network', level='Group', before='UNKNOWN', after='LIKELY (GSMFATHER or its upstream)', why="HalabTech names embed GSMFATHER's own service IDs 1351#/1352#.", tids=['W6-11', 'V7-21']),
    L(obj='GRP-S-109 Gsm Auth Tool; GRP-S-233 Setool; GRP-S-263/319 CF-Tools', level='Group', before='UNKNOWN', after='LIKELY (named intermediary)', why='Developer documents name the API partner / sole distributor / main distributor.',
      tids=['W5-76', 'W5-77', 'W5-75']),
    L(obj='GRP-S-136 AI Bot For Gsm Site', level='Group', before='UNKNOWN (not checked)', after='LIKELY (in-house)', why="HalabTech's chat is an in-house n8n service; client chat sub-domains exist.", tids=['V7-22', 'W1-04', 'W1-06']),
    L(obj='GRP-S-250 Laelo Samsung Unlock tool', level='Group', before='UNKNOWN (not checked)', after='LIKELY (Infinity direct)', why="SKU names attribute the tool to Infinity; HalabTech is an official Infinity distributor.", tids=[]),
    L(obj='GRP-S-260 HTD', level='Group', before='UNKNOWN (not checked)', after='LIKELY (HTD direct or in-house)', why='HTD is the SaaS behind store.halabtech.com; HalabTech resells its plans.', tids=['W1-03']),
    # Phase-5 finding-level changes
    L(obj='W3-03 (stream finding)', level='Finding (Phase 5)', before='LIKELY', after='DISPUTED', why='Date misread (MM-DD-YYYY).', tids=['W3-03', 'V7-08']),
    L(obj='W2-14 (stream finding)', level='Finding (Phase 5)', before='DISPUTED', after='UNKNOWN', why='Tier-discount caveat: cheaper competitors may be HalabTech dealers.', tids=['W2-14', 'V7-18']),
    L(obj='W6-08 (stream finding)', level='Finding (Phase 5)', before='LIKELY', after='DISPUTED', why='Direction contradicted by HalabTech-internal labels on Code-GSM.', tids=['W6-08', 'V7-10']),
    L(obj='W4-09 (stream finding)', level='Finding (Phase 5)', before='LIKELY', after='DISPUTED (rejected)', why="Store 'Details: api' label is non-discriminating.", tids=['W4-09', 'V7-07']),
    L(obj='W4-10 (stream finding: Hydra direct)', level='Finding (Phase 5)', before='STRONG', after='LIKELY', why='Vendor per-credit retail not re-confirmed by a second tool.', tids=['W4-10', 'V7-16']),
    L(obj='W2-03 (stream finding: GsmUnlockingStore MDM ratio)', level='Finding (Phase 5)', before='LIKELY', after='UNKNOWN', why='Two manual charm prices; ratio x1.425 outside computed-markup range.', tids=['W2-03', 'V7-03']),
    L(obj="V7-11, W7-05, W7-06, W7-10, W7-03, W7-08, W7-16 ('Miniutes' marker)", level='Finding text (Phase 5)', before='(unchanged confidence)', after='(unchanged confidence)',
      why="'Miniutes' withdrawn as a HalabTech marker (Dhru default).", tids=['W6-01']),
]

# --------------------------------------------------------------------------------------------------------------
# 8. Documented public APIs / integration statements (vendor-published; for the Website & Public API sheet)
# --------------------------------------------------------------------------------------------------------------
API_DOCS = [
    ('Cerberus Tool', 'https://cerberustoolpro.com/', "'A DHRU-compatible API for your reseller panel'", 'W5-72'),
    ('Apizu MDM Tool', 'https://apizutool.one', 'Reseller API for Dhru Fusion (R6 A2); HalabTech SUPER PREMIUM', 'W5-74'),
    ('SIM-UNLOCKER PRO', 'https://sim-unlocker.pro', 'Each reseller gets its own API to create users and add credits', 'W5-73'),
    ('GsmAuth.com / GsmDone.com', 'https://www.gsmauth.com/', "'GsmDone.com Provide Dhru Web API to Other websites For Recharge GsmAuth.com User Account Credits'", 'W5-76'),
    ('Venom Auth Tool = Ultra Auth Tool (white-label)', 'https://venomauthtool.com', "'Dhru Fusion-compatible API for resellers to transfer credits'", 'W5-85'),
    ('Eagle FRP Tool', 'https://eaglefrp.com/', "'Full API Server Integration' for master distributors", 'W5-39'),
    ('TMT Pro Tool', 'https://tmtprotool.com/reseller.php', "Premium Distributor tier: 'API access', 'Sub-reseller rights'", 'W5-24'),
    ('Mysterio FRP', 'https://www.mysteriofrp.com/', "Primary wholesale distributor 'with direct API access'; API integration tier", 'W5-80'),
    ('Fast Unlocking (NCK & UMT team server)', 'https://www.fastunlocking.co.uk/', "'direct support to all other servers APIs'", 'V7-15'),
    ('HTD CRM (store SaaS)', 'https://htdtech.dev/', "'Our platform supports integration with DHRU or HTD Scripts APIs'", 'W1-03'),
    ('HalabTech (own)', 'https://t.me/halabtech2', "Invites servers to connect by API; 'SYNC API' notices; DISTRIBUTOR page 'Web Owner' package", 'W1-09'),
]
