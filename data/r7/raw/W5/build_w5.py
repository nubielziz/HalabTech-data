# Builds r7/findings/W5.json for stream W5-longtail. Run: python3 -I build_w5.py <r7_dir>
import json, sys, os

R7 = sys.argv[1]
OUT = os.path.join(R7, 'findings', 'W5.json')
TSV = os.path.join(R7, 'raw', 'r6_not_checked_tool_groups.tsv')

T = {
 'PS': '2026-10-11T10:13Z', 'V1': '2026-10-11T10:17Z', 'V2': '2026-10-11T10:18Z', 'V3': '2026-10-11T10:19Z',
 'V4': '2026-10-11T10:20Z', 'V5': '2026-10-11T10:21Z', 'V6': '2026-10-11T10:21Z', 'V7': '2026-10-11T10:23Z',
 'V8': '2026-10-11T10:24Z', 'V9': '2026-10-11T10:24Z', 'FC1': '2026-10-11T10:25Z', 'FC2': '2026-10-11T10:26Z',
 'V10': '2026-10-11T10:26Z', 'S': '2026-10-11T10:27Z', 'V11': '2026-10-11T10:27Z', 'FC3': '2026-10-11T10:28Z',
 'V12': '2026-10-11T10:28Z', 'R6': '2026-10-11T02:0xZ (R6)'}
EXA = 'mcp__Exa__web_fetch_exa'; FC = 'mcp__Firecrawl__firecrawl_scrape'; PS = 'mcp__Parallel_Search__web_search'

# ---------------------------------------------------------------- tool log (every MCP call, in order)
tool_log = [
 ('mcp__Exa__agent_run', 'START batch A: 38 rows (Samsung/LG unlock tools + schematics/hardware), effort=high, outputSchema rows[group,vendor,official_site,reseller_page_url,halabtech_listed,halabtech_role_wording,distributors,sells_only_via_distributors,own_reseller_api_or_panel,evidence_url,evidence_excerpt,family_note]', True, 'runId agent_run_77b780eab2724abcb0f509c849b4ffc8'),
 ('mcp__Exa__agent_run', 'START batch B1: 40 rows (multi-SKU activation tools), effort=high, same schema', True, 'runId agent_run_e956c36d67964a9db405eeee1f30bbd0'),
 ('mcp__Exa__agent_run', 'START batch B2: 39 rows (misc credit/activation tools), effort=medium, same schema', True, 'runId agent_run_18346207c92b48b58912b0bffa21e657'),
 ('mcp__Exa__agent_run', 'START batch C1: 40 rows (Xiaomi/Realme auth & FRP tools 1), effort=medium, same schema', True, 'runId agent_run_6e89ba9b84c848afb71ccdffbce9a470'),
 ('mcp__Exa__agent_run', 'START batch C2: 40 rows (Xiaomi/Realme auth & FRP tools 2), effort=medium, same schema', True, 'runId agent_run_257a7f51c6414fe1b7e80fcc490fafc3'),
 (PS, 'objective: official sites/distributor pages of Yemeni Samsung/LG unlock tools (General Unlocker Pro, Alseery, Golden Unlocker, Fast Unlocker Pro, Tira, haliunlock) [5 of 6 queries used]', True, 'sim-unlocker.net/reseller (HALABTECH=Reseller; own Reseller API), haliunlock.com (GSM Main Reseller), general-unlocker.com (Sanaa), global-unlocker-pro.com/Reseller, vpunlocker.com (lists HalabTech Distributor)'),
 (PS, 'objective: developer/back office and distributors of RTC Tool, MTK GoGo, SimTool, GSMUnlock', True, 'rtc-tool.com resellers: HALABTECH Distributor WorldWide (Thai site); nothing for MTK GoGo/SimTool/GSMunlock vendors'),
 ('mcp__Exa__agent_run', 'POLL runId agent_run_77b780eab2724abcb0f509c849b4ffc8 (A)', True, 'still running'),
 (PS, 'objective: official sites of AlseerY Unlocker, Golden-Unlocker, Fast Unlocker Pro, T-Unlock, Laelo, Tira', True, 'fast-unlocker-pro.com (+967), golden-unlocker.com suspended (Tracxn), tiraunlocker.com (Ibb, Yemen), aliunlockers.com store strings'),
 ('mcp__Exa__agent_run', 'POLL runId agent_run_77b780eab2724abcb0f509c849b4ffc8 (A)', True, 'completed: 38 rows, 8 HT=yes, 2 HT=no, 60 searches, $0.50 (output saved to file, parsed with python3 -I)'),
 ('mcp__Exa__agent_run', 'POLL runId agent_run_e956c36d67964a9db405eeee1f30bbd0 (B1)', True, 'completed: 40 rows, 21 HT=yes, 2 HT=no, 60 searches, $0.50'),
 ('mcp__Exa__agent_run', 'POLL runId agent_run_18346207c92b48b58912b0bffa21e657 (B2)', True, 'completed: 39 rows, 7 HT=yes, 3 HT=no, 12 searches, $0.10'),
 ('mcp__Exa__agent_run', 'POLL runId agent_run_6e89ba9b84c848afb71ccdffbce9a470 (C1)', True, 'completed: 40 rows, 5 HT=yes, 0 HT=no, 12 searches, $0.10'),
 ('mcp__Exa__agent_run', 'POLL runId agent_run_257a7f51c6414fe1b7e80fcc490fafc3 (C2)', True, 'completed: 40 rows, 4 HT=yes, 0 HT=no, 12 searches, $0.10'),
 ('mcp__Exa__agent_run', 'START second pass D1: 40 unresolved rows (auth/FRP/misc), effort=high, same schema', True, 'runId agent_run_de856ebc342a45968ac582049a569200'),
 ('mcp__Exa__agent_run', 'START second pass D2: 40 unresolved rows (auth/FRP/misc), effort=high, same schema', True, 'runId agent_run_71dd3a66edd145d8abe47ebc446c98d1'),
 ('mcp__Parallel_Search__web_fetch', '20 reseller-page URLs (UST, Pulsar, Deep, GFT, Tira, General, Fast Unlocker, Turbo, Sim-Unlocker, RFT, OPlusPro, UFT, SmartTool, RootMagisk, BMT, MotoKing, KGFix, Fenix, tojo360, inmobile)', False, 'Error: Too Many Requests; switched to Exa fetch'),
 (EXA, 'V1: unlockservicetool.com, pulsarsync.com/resellers.php, deepunlocker.net/resellers.php, globalfrptool.com, tiraunlocker.com/resellers.php, general-unlocker.com/reseller/, fast-unlocker-pro.com, turboschematics.com, sim-unlocker.net/reseller, rftloader.com/resellers.html (maxCharacters 12000)', True, '9/10 lists rendered (sim-unlocker names not rendered); HalabTech present on all 9'),
 (EXA, 'V2: opluspro.net, uft-tool.com, smarttool.top/resellers_tab.php, rootmagisk.com/agents, bmt-pro.com/reseller, motokingprotool.com/resellers.php, kgfixtool.com/distributors_and_resellers.php, fenixtoolpro.com, tojo360.com, inmobile.info/ic/reseller.php', True, 'HalabTech present on all 10'),
 (EXA, 'V3: cftoolsid.com/reseller, apizutool.one/reseller.php, checkertr.com/resellers.html, tmtprotool.com/reseller.php, hijatekunloker.com, tfmtool.com/reseller, tera-tool.com/reseller, samuelcelular.com/resellers, shellmdm.com/resellers, gsmcode.pro/exynosFRP?lang=en', True, 'HalabTech present on all 10'),
 (EXA, 'V4: mdmfixtool.com/distributors_and_resellers, gsmfuture.in/resellers.php, nexapro.co.in/login/resellers.php, emmcpro.com/Sales/index.html, eaglemultitool.com, x-tool-pro.com/reseller.php, samprotool.com/resellers.php, egsmpro.com/resellers, eaglefrp.com, radexfrp.com', True, 'HalabTech present on all 10'),
 (EXA, 'V5: smartfrptool.com, dragon-frp.com/resellers.php, falconfrptool.com/reseller.php, xiaomiservicetool.com/reseller.php, xiaomirepairtool.com/reseller.php, galaxy-realme.com, mysteriofrp.com, wuxinji.com/sub-en4/Buy.html, worldlinkgsmpro.com, robytechtool.com', True, '6 positives verified; Mysterio, Wuxinji, WorldLinkGSM, Roby: HalabTech absent'),
 (EXA, 'V6: themagictool.net/resellers, guerratool.com/resellers, mfcbox.com/dealers/, krakenauthtool.org/buy.php, cp-tool.com/resellers.php, fastfrptool.com, easyauthtool.com, tunaprotool.com, xiaomiflasherpro.com, zhizhensolutions.com', True, 'CP Tool lists HALABCTECH (agent had unknown); Zhizhen WORLDWIDE partner mail = Halabtech.cert@gmail.com; 7 negatives; FastFRP partial render'),
 ('mcp__Exa__agent_run', 'POLL runId agent_run_de856ebc342a45968ac582049a569200 (D1)', True, 'completed: 40 rows, 8 HT=yes (GSM Family mapping rejected), 3 HT=no, 60 searches, $0.50'),
 ('mcp__Exa__agent_run', 'POLL runId agent_run_71dd3a66edd145d8abe47ebc446c98d1 (D2)', True, 'completed: 40 rows, 12 HT=yes (MDM FIX PRO mapping rejected), 1 HT=no, 60 searches, $0.50'),
 (EXA, 'V7: ah-tool.com, hxrutool.net/reseller.php, matauthtool.com/reseller.php, multiprotool.com/resellerlist/, xiaomispeedtoolpro.com/reseller.php, mobileprotool.com/resellers.php, falconmultitool.com, frpbosstool.com/seller.php, xiaomiauth.net/resellers_and_distributors.php, mifrp.com/resellers.php, repairfixauthtools.com/ourreseller.php, androidauthtool.com/reseller.php', True, 'HalabTech present on 11; multiprotool names not rendered (re-checked with Firecrawl)'),
 (EXA, 'V8: mrauthtool.com/team, mifixpro.com/resellers, xiaomifiretool.com, nextgauthtool.net/reseller.php, xiaomikingtool.com/resellers.html, iproauthtool.com/reseller.php, miuitool.com/resellers.php, home.lazyloader.in, toniprotool.com, xiaomipaid.com, mifrptool.com, gsmauth.com, venomauthtool.com, ultraauth.org', True, '5 positives + iPro ambiguous; MIUI/Lazy/TONI/XiaomiPaid/MIFRPTOOL absent; GsmAuth names GsmDone.com Dhru API partner; Venom/Ultra identical Dhru-API template'),
 (EXA, 'V9: cerberustoolpro.com, knoxwizard.com, pixelprotool.com/resellers/, motounlocktool.com/seller, niceunlockertool.net, kingunlock.net/resellerlist.html, t-unlock.com/resellers/, qcdma-tool.com/p/sellers-agents.html, gaprologin.com/resellers, alientool.app/resellers.html, arabfrp.com/Profile/ArabFRPTool/, tool.emmc-ufs.com/en/', True, 'lists mostly JS (not rendered); errors: motounlocktool HTTP 500, kingunlock & t-unlock CRAWL_UNKNOWN_ERROR, gaprologin HTTP 502'),
 (FC, 'https://www.sim-unlocker.net/reseller (markdown, waitFor 3000, maxAge 0)', True, 'HALABTECH under Other Resellers; Top Resellers HaliUnlock/Ady/Unlock King/Fast Unlockers; own Reseller API'),
 (FC, 'https://cerberustoolpro.com/ (markdown, maxAge 0)', True, '355k chars saved to file; seller section: A DHRU-compatible API for your reseller panel'),
 (FC, 'https://knoxwizard.com/ (markdown, waitFor 4000, maxAge 0)', True, 'HalabTech Official Distributor, Distributor / Reseller Worldwide'),
 (FC, 'https://pixelprotool.com/resellers/ (markdown, waitFor 4000, maxAge 0)', True, 'HALABTECH Master, Official Global Distributor'),
 (FC, 'https://cerberustoolpro.com/partners (markdown, waitFor 4000, maxAge 0)', True, '6 partners; HALABTECH Special Distributor'),
 (FC, 'https://multiprotool.com/resellerlist/ (markdown, maxAge 0)', True, 'HALABTECH Worldwide Distributor (Turkey)'),
 (FC, 'https://kingunlock.net/resellerlist.html', False, 'DNS resolution failed'),
 (FC, 'https://t-unlock.com/resellers/', False, 'DNS resolution failed'),
 (EXA, 'V10: haliunlock.com, gsmunlock.net, simtool.net, artemis2.vip, gsmhelptool.com, muslimodin.com, f-keytool.net, sam-token.com, zxwtools.com/en/buy.html, w2rsolutions.in/user/reseller.php, mesallah.com/resellers, gsmorion.com', True, 'haliunlock contact only; gsmunlock.net = Tajik GSM store; simtool.net = unrelated Chinese tile site; ZXW 2 agents (no HalabTech); others no names'),
 ('mcp__Exa__web_search_exa', 'MTK GoGo unlock tool official website resellers SIMTool Thailand credits create new user', True, 'mtkgogo.com referenced by stores; naming posted by Best4unlock on GSM-Forum (2022-11-12); no vendor reseller list'),
 (EXA, 'V11: mtkgogo.com, gpixel.pro, imeiplus.com, fdtool.com.br, kgprotoolnextgen.com, multiunlock.com, gawansmirtunlockerprotool.com, frpunlocktool.com, pixelservicetool.com, laelotool.com, idevicepro.ru, typhontool.com/resellers', True, 'mtkgogo CRAWL_UNKNOWN_ERROR; Pixel Service Tool: DHRU Fusion reseller API; Typhon: No resellers found; FRP Unlock Tool = Tuna template'),
 (FC, 'https://www.qcdma-tool.com/p/sellers-agents.html', True, 'Blogger page; agent names not rendered'),
 (FC, 'https://www.gaprologin.com/resellers', False, 'All scraping engines failed'),
 (FC, 'https://alientool.app/resellers.html', True, 'Halabtech Top Reseller Verified Worldwide'),
 (FC, 'https://mtkgogo.com/', False, 'DNS resolution failed'),
 (EXA, 'V12: files.setool.net/support/SETool2/, penguintool.com, ohauthtool.com, rbm-borneo.com, xfrppro.com/reseller.php, mi-bypass.com/resllers/, xiaomibeast.com, firefrptool.com, mrprofixer12.com, embauthtool.com, oneclick-tool.com, soulauth.com', True, 'SETool distributor GsmEasy only; Penguine main distributor Activeunlocker; OH AUTH: verified Dhru Fusion partners (dynamic); OneClick Tool = Sanaa, Al Qasr Street; xfrppro & mi-bypass SOURCE_NOT_AVAILABLE'),
]
tool_log = [dict(tool=a, input=b, ok=c, note=d) for a, b, c, d in tool_log]

# ---------------------------------------------------------------- vendor listings (all verified by R7 fetch unless noted)
# key: groups, entity, site, url, role, tier, excerpt, t, tool, conf, dists, only, api, notes, supports
L = []
def add(**k): L.append(k)

add(groups=['UNLOCK SERVICE TOOL ( UST )'], entity='UnlockServiceTool (Xiaomi/Realme multi-auth tool)', site='unlockservicetool.com', url='https://unlockservicetool.com/',
    role="Distributor/Reseller WorldWide - the only partner shown besides 'Owner'", tier='SOLE',
    excerpt='Authorized Resellers Purchase official credits securely from our verified global distributor partners. UN Owner HA Halab Tech Distributor/Reseller WorldWide',
    t='V1', tool=EXA, conf='CONFIRMED', dists='Halab Tech only (plus Owner)', only='yes (FAQ: contact any authorized reseller listed on the site)', api='unknown', notes='')
add(groups=['Pulsarunlock'], entity='Pulsarunlock (pulsarsync.com)', site='pulsarsync.com', url='https://pulsarsync.com/resellers.php',
    role="'Our Resellers' flat list: Halab Tech - Worldwide", tier='FLAT', excerpt='Halab Tech Halab Tech Worldwide ##### Contact Information GSM FASTEST',
    t='V1', tool=EXA, conf='CONFIRMED', dists='no tiers; also Click Unlock, TerritorioUnlock, ady unlockers, Full Unlock MX, GSM FASTEST, GMS RESELLER, Ethioserver, OHIDERA, Power Unlock, esim unlocker', only='unknown', api='unknown', notes='')
add(groups=['Deep Unlocker Tool'], entity='Deep Unlocker (deepunlocker.net)', site='deepunlocker.net', url='https://deepunlocker.net/resellers.php',
    role='Distributor/Reseller WorldWide (first of 4 authorized resellers)', tier='DIST',
    excerpt='Halabtech Distributor/Reseller WorldWide https://server.halabtech.com/contactus https://telegram.me/htsupport server.halabtech.com',
    t='V1', tool=EXA, conf='CONFIRMED', dists='GSMFASTEST, imeiFree, ohideraunlocker', only='unknown', api='unknown', notes='')
add(groups=['Global Frp Tool (GFT)'], entity='Global FRP Tool (globalfrptool.com)', site='globalfrptool.com', url='https://globalfrptool.com/',
    role="#4 'HalabTechServer' in the numbered 'Authorized Distributors' list (per-entry label not rendered)", tier='DIST',
    excerpt='### 3. AdyUnlocker +6 ### 4. HalabTechServer', t='V1', tool=EXA, conf='CONFIRMED',
    dists='Source For Unlock (Distributor), Global Unlocker, AdyUnlocker, DHIQAR-SERVER.COM, AfghanUnlock, Clean Unlocker, IMEI STAR, POWER GSM, GSM-T-TOOL ...', only='unknown', api='unknown',
    notes='Vendor public price 1 Credit = 1.00 USDT; HalabTech sells GFT credits at $0.998-0.999 (10:03Z), i.e. at vendor list price - HalabTech must buy below list (distributor discount).')
add(groups=['Tira unlocker'], entity='Tira Unlocker (Ibb, Yemen)', site='tiraunlocker.com', url='https://www.tiraunlocker.com/resellers.php',
    role="RESELLERS: 'HALABTECH Turky-Syria-Iraq' (the only DISTRIBUTOR is Ady Unlocker)", tier='RES',
    excerpt='#### WorldWide HALABTECH Turky-Syria-Iraq #### WorldWide Easy-Unlocker worldwide', t='V1', tool=EXA, conf='CONFIRMED',
    dists='DISTRIBUTOR WorldWide: Ady Unlocker (sole); resellers incl. Speed Unlocker, AllUnlocker, GSM-T-TOOL, Alseery SofT Yemen, Alwahdah Yemen', only='unknown', api='unknown',
    notes='Resolves R6 A2 negative (Tira list not found). HalabTech is reseller-tier here.', supports='A2 negative (Tira) resolved')
add(groups=['General Unlocker Pro'], entity='General Unlocker (General Team, Al Qasr Street, Sanaa, Yemen)', site='general-unlocker.com', url='https://general-unlocker.com/reseller/',
    role="'WorldWide distributor' - 'HALABTECH (Distributor And Reseller)'; not one of the 'Main Distributor' entries", tier='DIST',
    excerpt='## HALABTECH WorldWide distributor HALABTECH (Distributor And Reseller) (Distributor And Reseller Most Welcome)', t='V1', tool=EXA, conf='CONFIRMED',
    dists='Main Distributors: haliunlock (+967777600067), Speed Unlocker (+967775177518), All Unlocker (+967777563332 / +962789940944); GSM-T-TOOL EXCLUSIVE World Wide; adyunlocker; Easy-Firmware',
    only='yes (homepage, search snippet: the reseller will open a new account for you)', api='unknown (agent claimed yes; not verified)', notes='')
add(groups=['Fast Unlocker Pro'], entity='Fast Unlocker Pro (Fast Unlocker Team, Yemen +967)', site='fast-unlocker-pro.com', url='https://fast-unlocker-pro.com/',
    role="'Our Distributers' list (3rd entry, after adyunlocker and SALIF GSM)", tier='DIST',
    excerpt='Through our authorized agents and distributors around the world auto API 24/7 adyunlocker || Address : Dubai pay with: SALIF GSM pay with: halabtech',
    t='V1', tool=EXA, conf='CONFIRMED', dists='adyunlocker (first), SALIF GSM, gsm-t-tool.com, click-unlock, easy-unlocker, alcaptainunlock ... (~100 entries)', only='unknown (vendor also sells credits for crypto)', api="yes ('auto API 24/7' for distributors)",
    notes="Direct crypto-sale instructions: 'After Payment Send (Payment ScreenShot) to WhatsApp, +12816728384' - the number ADY Unlocker publishes on SmartTool, Tera, MotoKing and KGFix pages.")
add(groups=['Turbo tool (Hardware)'], entity='TurboSchematics', site='turboschematics.com', url='https://turboschematics.com/',
    role='Authorised Distributor - WorldWide (1 of 6 authorised distributors)', tier='DIST', excerpt='### HalabTech Authorised Distributor WorldWide Visit website WhatsApp ### ADY Unlocker Authorised Distributor WorldWide',
    t='V1', tool=EXA, conf='CONFIRMED', dists='SSS GSM, AppleFix Solutions, Express Unlocking, UnlockerBD, ADY Unlocker', only="yes ('only purchase activation keys from the official resellers listed above')", api='unknown', notes='')
add(groups=['Samsung Sim-Unlocker'], entity='SIM-UNLOCKER PRO (owner contact Mohsin, +923002525532)', site='sim-unlocker.net', url='https://www.sim-unlocker.net/reseller',
    role="'Other Resellers' - Reseller, Address WorldWide (not a 'Top Reseller')", tier='RES',
    excerpt='# **Other Resellers** ### Reseller ### HALABTECH ### Address :WorldWide', t='FC1', tool=FC, conf='CONFIRMED',
    dists='Top Resellers: HaliUnlock (Yemen / Worldwide), Ady Unlocker, Unlock King, Fast Unlockers', only='unknown', api="yes ('BE RESELLER BY YOUR OWN API AND SELL CREDITS ... Get Your Own Reseller API Create users / Add credits')", notes='Exa fetch did not render names; Firecrawl did.')
add(groups=['RFT Loader'], entity='RFT Loader (rftloader.com)', site='rftloader.com', url='https://rftloader.com/resellers.html',
    role='World-Wide Distributor (one of 4 top-tier partners)', tier='TOP4', excerpt='🌍 World-Wide Distributor Halabtech.com Worldwide halabtech.com Contact Us Telegram',
    t='V1', tool=EXA, conf='CONFIRMED', dists='World-Wide Distributors: Softsoln.com, Gsmninja.com, Adyunlocker.com; Official Distributors: Smartunlocker.in, Mdunlocker.com, Soft-unlock.com, AmRomTech, Appleunlockers, Gsmultimate, gsmfastpro, Dhiqar-service',
    only="yes ('Important - Buy Only from Official Resellers Listed Below')", api='unknown', notes='Same template/text as gsmfuture.in (see family).', supports='C-11 (RapidFlashTool lists HalabTech) - related RFT brand')
add(groups=['OPlusProLogin'], entity="OPlusPro (owner shown as 'FalconMultiTool Team')", site='opluspro.net', url='https://opluspro.net/',
    role='Distributor WorldWide (Main Distributor is GSM Manager)', tier='DIST',
    excerpt='### GSM Manager Main Distributor ### FalconMultiTool Team Owner ### GSMPURE || PUREUNLOCKER Distributor WorldWide ### Halab Tech Distributor WorldWide',
    t='V2', tool=EXA, conf='CONFIRMED', dists='Main Distributor GSM Manager; GSMPURE, dmunlocker.com, IMEISTAR, FRP King Server, Mhmd frp (distributors)', only='unknown', api='unknown', notes='Identical roster on falconmultitool.com.', supports='D-22 (GSM Manager resells HalabTech credits)')
add(groups=['UFT-Tool'], entity='UFT-Tool (Yemeni tool; IPCC files for Yemen)', site='uft-tool.com', url='https://uft-tool.com/',
    role="'وكلائنا المعتمدون' (our accredited agents) - HALAB TECH listed 3rd", tier='FLAT',
    excerpt='## وكلائنا المعتمدون الادريسي كارد Hali Unlock HALAB TECH ابراهيم الحوات All Unlocker Speed Unlocker', t='V2', tool=EXA, conf='CONFIRMED',
    dists='no tiers; Hali Unlock, All Unlocker, Speed Unlocker, Al-Amery Tech, Global Unlocker Store and Yemeni card shops', only='unknown', api='unknown',
    notes='Vendor plans $15/3m, $20/6m, $30/12m vs HalabTech $14.40/$19.55/$28.75 (10:03Z) - HalabTech at 0.96-0.98 of vendor list.')
add(groups=['Smart Tool Pro Tool'], entity='SmartTool Pro (smarttool.top)', site='smarttool.top', url='https://smarttool.top/resellers_tab.php',
    role='Official worldwide distributor', tier='DIST', excerpt='### halabtech Worldwide · Asia · Middle East Official worldwide distributor with comprehensive support in multiple languages.',
    t='V2', tool=EXA, conf='CONFIRMED', dists='frpkingaksumon, BaseUnlock, CREMOGSM, ADYunlocker, OrionGsm, Hellounlocker, Ethioserver, gsmninja ...; LopezGsm described as direct sales from the development team', only='unknown', api='unknown (agent claimed yes)',
    notes='Product mapping by name (HalabTech SKUs: Smart Tool Pro Activation 10h-12m + Credits). Not the CellTool/Smart Tool WW product from R6 A2-22.')
add(groups=['RootMagisk.com Packages'], entity='RootMagisk', site='rootmagisk.com', url='https://rootmagisk.com/agents',
    role='Distributor (1 of 3)', tier='DIST', excerpt='## Distributors Halabtech Distributor Phone Email Website Contact Legitunlocks.com Distributor',
    t='V2', tool=EXA, conf='CONFIRMED', dists='Legitunlocks.com, GsmServer', only='unknown', api='unknown', notes='')
add(groups=['BMT Pro Tool'], entity='BMT Pro (bmt-pro.com)', site='bmt-pro.com', url='https://bmt-pro.com/reseller',
    role="first entry, labelled 'Pakistan - Reseller'", tier='RES', excerpt='# RESELLER & DISTRIBUTOR Official Partners of BMT PRO Worldwide ## HALABTECH Pakistan - Reseller',
    t='V2', tool=EXA, conf='CONFIRMED', dists='all entries labelled Reseller (Clean Unlocker, GSM-T-TOOL, Gsm Scene, GSMUnlockInfo, GSM Paid, GSMFASTEST, Habesha, UnlockerBD, IMEISTAR, asunlocker, IDUnlocker)', only='unknown', api='unknown',
    notes="Country label 'Pakistan' for HalabTech is likely a vendor copy error. Same page template/roster as iproauthtool.com.")
add(groups=['Moto King Pro'], entity='MotoKingPRO', site='motokingprotool.com', url='https://motokingprotool.com/resellers.php',
    role='VERIFIED partner (no tier)', tier='FLAT', excerpt='Halab Tech VERIFIED Phone +963992951910 WhatsApp +963992951910 Telegram @htsupport',
    t='V2', tool=EXA, conf='CONFIRMED', dists='31 verified partners (ADY UNLOCKER first; GSM Server, FRP King, Territorio Unlock ...)', only="yes ('Buy only from this official list')", api='unknown', notes='Resolves R6 A2 negative (list not retrievable).', supports='A2 negative (Moto King Pro) resolved')
add(groups=['KGFix Tool'], entity='KGFixTool', site='kgfixtool.com', url='https://kgfixtool.com/distributors_and_resellers.php',
    role="listed 3rd under 'Distributors and Resellers' (no per-entry label)", tier='FLAT', excerpt='## HalabTech - HalabTech - HalabTech - +249116472371 - @htsupport',
    t='V2', tool=EXA, conf='CONFIRMED', dists='Topunlocksite, Adyunlocker, FRP King Server, Unlock Easy, GSM-T-TOOL, Power GSM ...', only='unknown', api='unknown',
    notes='HalabTech entry uses a Sudan number (+249116472371) with @htsupport - compare R6 D-11 (AnonySHU, +249).')
add(groups=['Fenix Utility Pro'], entity='FENIX TOOL PRO (fenixtoolpro.com)', site='fenixtoolpro.com', url='https://fenixtoolpro.com/',
    role="'Distribuidores Oficiales' (no label)", tier='DIST', excerpt='#### Latin Unlockers 🌐 Internacional / Brasil #### HalabTech #### Punto Digital 🌐 Internacional / Colombia',
    t='V2', tool=EXA, conf='CONFIRMED', dists='Darkness Gsm, Latin Unlockers, Punto Digital, Legend Unlocks', only='no (vendor sells activations directly for USDT)', api='unknown',
    notes='Vendor monthly activation 17 USDT, credits 1 USDT; HalabTech 1 Month $14.99, credits $0.969 (below vendor retail). Product mapping by name (Fenix Utility Pro = Fenix Tool Pro).')
add(groups=['tojo360 Tool'], entity='360 TOOL (tojo360.com, Tanzania +255)', site='tojo360.com', url='https://tojo360.com/',
    role='Worldwide Distributor', tier='DIST', excerpt='### HalabTech Worldwide Distributor https://server.halabtech.com/ @htsupport Contact via WhatsApp',
    t='V2', tool=EXA, conf='CONFIRMED', dists='FRP King Server, UnlockerBD, Ohideraunlocker, GSMUnlockInfo, GSMFastest, GMS RESELLER, GSM MUNNA, GSM HELPER', only='unknown', api='unknown', notes='Identical site template to hijatekunloker.com (HSPRO TOOL).')
add(groups=['inmobile Activation'], entity='inmobile (IC & hardware fault finder; vendor WhatsApp +98)', site='inmobile.info', url='https://inmobile.info/ic/reseller.php',
    role='Reseller - WorldWide (1 of 4)', tier='FLAT', excerpt='#### WorldWide HALABTECH ##### Copyright 2016 - 2026', t='V2', tool=EXA, conf='CONFIRMED',
    dists='UNLOCK (unlock.ws), Z-UNLOCK, UnlockrepairserviceLLC', only='unknown', api='unknown', notes='')
add(groups=['CF-Tools Activation', 'CF-Tools Credit'], entity='CF Tools (ChopelFlasher, cftoolsid.com)', site='cftoolsid.com', url='https://cftoolsid.com/reseller',
    role='Worldwide Reseller (the single Main Distributor is AppleUnlocker)', tier='RES',
    excerpt='#### HalabTech Worldwide Reseller Reseller Welcome Website: server.halabtech.com Telegram: @HTSupport', t='V3', tool=EXA, conf='CONFIRMED',
    dists='Main Distributor: AppleUnlocker (appleunlockers.com, +8801757574757); UnlockerBD and GSMUnlockInfo also country distributors', only='unknown', api='yes (R6 A2: terms describe Distributor->Reseller tiers with DHRU Fusion API)',
    notes='Updates R6 A2 negative (HalabTech position unknown).', supports='A2 negative (CF-Tools) updated')
add(groups=['Apizu Tool'], entity='Apizu MDM Tool (apizutool.one, Tanzania)', site='apizutool.one', url='https://apizutool.one/reseller.php',
    role='SUPER PREMIUM (top tier, with FRP King Server, CleanUnlocker, TopUnlockSite247)', tier='TOP', excerpt='### HalabTech SUPER PREMIUM International Hub English',
    t='V3', tool=EXA, conf='CONFIRMED', dists='SUPER PREMIUM: FRP King Server, CleanUnlocker, TopUnlockSite247; Resellers: Unlock Easy, UnlockerBD, Jara Unlocker, GSM Efrahim ...', only='unknown', api='yes (R6 A2: Reseller API for Dhru Fusion, apizutool.one/reseller-api/docs.php)',
    notes='Updates R6 A2 negative (no list found).', supports='A2 negative (Apizu) updated')
add(groups=['CheckerTR PRO'], entity='CheckerTR PRO', site='checkertr.com', url='https://checkertr.com/resellers.html',
    role="Worldwide Distributor in the 'Main distributors' section", tier='TOP', excerpt='### HalabTech Worldwide Distributor Worldwide Global Sales and Support Visit Website Telegram Support WhatsApp Contact',
    t='V3', tool=EXA, conf='CONFIRMED', dists='Main distributors: VIP Pro Support (CheckerTR Main Sales, +905302285200), Net Unlocker (Main Seller); resellers Unlock Bayi, unlockergroup; channels offunlock, IMEIveServer', only='unknown', api='unknown', notes='')
add(groups=['TMT Pro Tool'], entity='TMT Pro Tool', site='tmtprotool.com', url='https://tmtprotool.com/reseller.php',
    role='Big Distributor - the only entry in the top tier', tier='SOLE', excerpt='#### Big Distributors 1 ###### Halab Tech Big Distributor Worldwide @htsupport https://server.halabtech.com/contactus',
    t='V3', tool=EXA, conf='CONFIRMED', dists='Distributors (1): FRTECH; 17 Authorized Resellers incl. Adyunlocker', only='unknown', api="yes (Premium Distributor tier: 'API access', 'Sub-reseller rights'; Enterprise: 'Full API access')", notes='')
add(groups=['HSPRO TOOL Activation'], entity='HSPRO TOOL (hijatekunloker.com, GSM HIJATEK, Tanzania)', site='hijatekunloker.com', url='https://hijatekunloker.com/',
    role='HALABTECH DISTRIBUTOR/RESSELLER WORLDWIDE', tier='DIST', excerpt='#### HALABTECH DISTRIBUTOR/RESSELLER WORLDWIDE Website: "https://server.halabtech.com Contact: https://server.halabtech.com/contactus',
    t='V3', tool=EXA, conf='CONFIRMED', dists='FRP King Server, UnlockerBD, ohideraunlocker, GSM UNLOCK SERVER, Md Abdur Razzak, GSM-T-TOOL, GMS RESELLER, MUDY MOBILE TECH', only='unknown', api='unknown', notes='Identical template to tojo360.com.')
add(groups=['TFM Pro tool'], entity='TFMTool', site='tfmtool.com', url='https://tfmtool.com/reseller',
    role='Distributor (Country WorldWide)', tier='DIST', excerpt='#### HALABTECH (Distributor) | Name | HALABTECH |', t='V3', tool=EXA, conf='CONFIRMED',
    dists='GSM AFRICA, MUKESH RAJ (GsmGenesis), GSMFASTEST, ADY unlocker, fixunlocker/TFM Server, AllTimeUnlocker, CleanUnlocker, IRAQ SERVER, Ethioserver (distributors); GSM Server, MartView, Easy-Firmware (resellers)', only='unknown', api='unknown', notes='')
add(groups=['Tera Tool'], entity='Tera Tool', site='tera-tool.com', url='https://www.tera-tool.com/reseller',
    role='Distributor - World Wide', tier='DIST', excerpt='#### Distributor #### HALABTECH - World Wide 🌏 - Website: server.halabtech.com', t='V3', tool=EXA, conf='CONFIRMED',
    dists='GsmNetSupport (Turkey), ADYunlocker, GsmGenesis (India), Unlock Easy', only='unknown', api='unknown', notes='Resolves R6 A2 negative (list not retrievable).', supports='A2 negative (Tera Tool) resolved')
add(groups=['RDPower Tools'], entity='RDPower by Samuel Celular', site='samuelcelular.com', url='https://samuelcelular.com/resellers',
    role='authorized reseller - Worldwide (Turkey, Syria, Arabic countries)', tier='FLAT', excerpt='### HALABTECH Worldwide (Turkey, Syria, Arabic countries) ### UnlockAllGSM',
    t='V3', tool=EXA, conf='CONFIRMED', dists='25 resellers (mostly Dominican Republic) + ADYunlocker, IMEISTAR', only='unknown', api='unknown', notes='')
add(groups=['Shell Tool Activation'], entity='SHELLTOOL (shellmdm.com)', site='shellmdm.com', url='https://www.shellmdm.com/resellers',
    role='Verified authorized reseller - Worldwide', tier='FLAT', excerpt='HALABTECH Worldwide 🚀 The Best Server — Trusted, Fast & Best Prices', t='V3', tool=EXA, conf='CONFIRMED',
    dists='CLICK UNLOCK SAS, Adyunlocker, Unlockeasy, genuineunlocker, FRP King Server (Distributor), GMS RESELLER, Ethioserver ...', only='unknown', api='unknown', notes='')
add(groups=['GSMCode.Pro Tools'], entity='GSMCode.PRO', site='gsmcode.pro', url='https://gsmcode.pro/exynosFRP?lang=en',
    role="'Official Authorized Distributors' - Verified, Worldwide / Syria", tier='DIST', excerpt='### HalabTech Worldwide / Syria Apple AIO BlackScreen Exynos Tool',
    t='V3', tool=EXA, conf='CONFIRMED', dists='Adyunlocker, EGY Unlockers, Petrock Biz, amrr-unlocker.com', only='unknown', api='unknown', notes='HalabTech SKUs are GCPro Black Screen licences.')
add(groups=['MDMFix Tool'], entity='MDMFix Tool (mdmfixtool.com)', site='mdmfixtool.com', url='https://www.mdmfixtool.com/distributors_and_resellers',
    role="first entry under 'Distributors and Resellers'", tier='DIST', excerpt='## HalabTech - HalabTech - HalabTech - +963992951910 - @htsupport',
    t='V4', tool=EXA, conf='CONFIRMED', dists='GSM-T-Tool, ZsTeamServer, AdyUnlocker, GsmGenesis, cleanunlocker, TopUnlockSite, TerritorioUnlock, FRP King, AsUnlocker, Gsm Africa ...', only='unknown', api='unknown', notes='Not the same product as HalabTech group MDM FIX PRO (MFP TOOL).')
add(groups=['Gsm Future Tool'], entity='GSM Future Tool (GFT OTP, gsmfuture.in)', site='gsmfuture.in', url='https://gsmfuture.in/resellers.php',
    role='Distributor', tier='TOP4', excerpt='Distributor Halabtech.com server.halabtech.com/ WhatsApp Telegram', t='V4', tool=EXA, conf='CONFIRMED',
    dists='Gsmninja.com, Softsoln.com, Adyunlocker.com, unlock.su, GsmDelhi.com (Distributors); Gmsreseller.com', only="yes ('Always purchase GFT OTPs from the official resellers listed on this page only')", api='unknown (credits transferred automatically after ordering on a reseller site)', notes='Same template/text as rftloader.com.')
add(groups=['Nexa Pro Tool'], entity='Nexa Pro Tool (nexapro.co.in)', site='nexapro.co.in', url='https://nexapro.co.in/login/resellers.php',
    role='Official Distributor', tier='DIST', excerpt='## Distributors Our Official Distributors with Worldwide Reach ### NeXaPro Distributor Worldwide ### GsmCredit ### AdyUnlocker ### HALABTECH',
    t='V4', tool=EXA, conf='CONFIRMED', dists='NeXaPro, GsmCredit, AdyUnlocker, GsmSekhar, GsmNinja, GsmTrick, Gsm Ultimate, APNA GSM', only='unknown', api='unknown (agent claimed yes)', notes='Group also contains an unrelated SKU (Nexus Service Tool Realme Token).')
add(groups=['DT PRO TOOL'], entity='DTpro (emmcpro.com)', site='emmcpro.com', url='http://emmcpro.com/Sales/index.html',
    role='Distributor | Worldwide', tier='DIST', excerpt='Halabtech - •Distributor | Worldwide - E-mail: info@halabtech.com - WebSite : https://server.halabtech.com',
    t='V4', tool=EXA, conf='CONFIRMED', dists='GsmServer, ADYunlocker, Gsm Anik (Appleunlockers), GSM Africa, GSMFastest, GSMUnlockInfo (distributors)', only="partial ('Buying from official resellers guarantees our support')", api='unknown',
    notes='Resolves R6 A2 negative (SPA returned homepage only).', supports='A2 negative (DT Pro) resolved')
add(groups=['Eagle Multi Tool'], entity='Eagle Multi Tool (EMT, eaglemultitool.com)', site='eaglemultitool.com', url='https://eaglemultitool.com/',
    role="Distributor ('Authorized Distributors', 1 of 6)", tier='DIST', excerpt='Distributor ### Halab Tech https://server.halabtech.com/contactus', t='V4', tool=EXA, conf='CONFIRMED',
    dists='AKUNLOCKER, Salif GSM, eSimUNlocker (Distributors); GSM MAMU, GsmQatar (Resellers)', only='unknown', api='yes (dedicated reseller panel for Realme services)', notes='Same white-label template as xiaomipaid.com.')
add(groups=['X-Tool PRO'], entity='X-Tool Pro (x-tool-pro.com)', site='x-tool-pro.com', url='https://x-tool-pro.com/reseller.php',
    role="'Authorized Resellers' (no label; AllTimeUnlocker is the labelled Distributor)", tier='FLAT',
    excerpt='# Authorized Resellers AllTimeUnlocker Distributor VERIFIED FRP King Server Martlobs GSM Ra1n Unlocker DHIQAR SERVER. COM(Salam Unlocker) Halab Tech',
    t='V4', tool=EXA, conf='CONFIRMED', dists='AllTimeUnlocker (Distributor)', only='unknown', api='unknown', notes='Resolves R6 A2 negative (/reseller looked like a login panel).', supports='A2 negative (X-Tool Pro) resolved')
add(groups=['Sampro A.i.O'], entity='SAMPRO Tool (author Mahmoud Salah)', site='samprotool.com', url='https://samprotool.com/resellers.php',
    role='Authorized Reseller (first of 13)', tier='FLAT', excerpt='13 Total Resellers 10 Countries 24/7 Support ### HalabTech - Website - Facebook - @htsupport',
    t='V4', tool=EXA, conf='CONFIRMED', dists='GEM FLASH, smart1phone, WETSCOMGSM, Easy-unlocker, FASTNCK ...', only='unknown', api='unknown', notes='')
add(groups=['E-GSM'], entity='E-GSM TOOL (egsmpro.com)', site='egsmpro.com', url='https://www.egsmpro.com/resellers',
    role='(RESELLER), Country SYRIA-TURKEY', tier='RES', excerpt='## HALAB TECH About : (RESELLER) Telegram : telegram.me/HTSupport Whatsapp : halabtech.com/contactus Country : SYRIA-TURKEY',
    t='V4', tool=EXA, conf='CONFIRMED', dists='Distributors: AHMET USTA (Turkey), GSM AFRICA, GSM Server, GsmPaid, GsmSalman, AdyUnlocker', only='unknown', api='unknown', notes='HalabTech SKU mentions egsmkey.com (E-GSM KEY).')
add(groups=['Eagle Frp'], entity='EAGLE FRP TOOL (eaglefrp.com)', site='eaglefrp.com', url='https://eaglefrp.com/',
    role='VERIFIED MASTER DISTRIBUTOR WORLDWIDE (one of two, with adyunlocker)', tier='TOP',
    excerpt='VERIFIED MASTER DISTRIBUTOR WORLDWIDE SERVICE ### HALABTECH SERVER Address: WorldWide / Global Service Official Worldwide Distributor & Reseller for Eagle FRP Tool.',
    t='V4', tool=EXA, conf='CONFIRMED', dists='Master: HALABTECH, adyunlocker; Distributor: sadik naji (GSM SDK, Iraq); Resellers: Gsm Imran Yasin, GSM SKB, nicegsm, Legend Unlocks', only='unknown',
    api="yes ('Full API Server Integration' for master distributors; 'Website Partner ... integrate Eagle FRP API directly into their own site')", notes='')
add(groups=['RADEX FRP TOOL'], entity='RADEX FRP Tool (radexfrp.com)', site='radexfrp.com', url='https://radexfrp.com/',
    role="tagged 'reseller', described '(Distributor And Reseller)'", tier='RES', excerpt='reseller ### HALAB TECH (Distributor And Reseller) reseller ### OFFUNLOCK (Distributor And Reseller)',
    t='V4', tool=EXA, conf='CONFIRMED', dists="distributors: Radex, Dost Service (+90 507 456 05 08); resellers IMEI ve SERVER, Unlock Bayi, UNLOCKERGROUP, OFFUNLOCK, Azaad Unlockers", only="yes ('Contact your reseller or administrator to add credit')", api='unknown', notes='')
add(groups=['Smart Frp Tool'], entity='Smart FRP Tool (smartfrptool.com)', site='smartfrptool.com', url='https://www.smartfrptool.com/',
    role="'Official Resellers' - first entry (no label)", tier='FLAT', excerpt='## Official Resellers Purchase credits from our trusted and verified resellers worldwide. ### Halab Tech ### Ady Unlocker',
    t='V5', tool=EXA, conf='CONFIRMED', dists='Ady Unlocker, Clean Unlocker, DhiQar-Service (Distributor), Gsm Fast Pro (Distributor), GSM Ultimate, Gsm Ninja, GOJO (Distributor)', only="yes (FAQ: contact any of our official resellers to purchase credits)", api='unknown', notes='')
add(groups=['Dragon Frp Tool'], entity='Dragon FRP Tool (dragon-frp.com)', site='dragon-frp.com', url='https://dragon-frp.com/resellers.php',
    role='Distributor', tier='DIST', excerpt='### HalabTech Distributor ### FRP King Server Distributor', t='V5', tool=EXA, conf='CONFIRMED',
    dists='ADYunlocker (Worldwide Seller), GSM-T-TOOL (WorldWide Distributor), FRP King Server, ohideraunlocker, Ethioserver, UnlockTrue', only='unknown', api='unknown', notes='')
add(groups=['Falcon FRP Tool'], entity='FalconFRPTool (falconfrptool.com)', site='falconfrptool.com', url='https://falconfrptool.com/reseller.php',
    role="listed under 'Our Trusted Distributors'", tier='DIST', excerpt='### GSMNXT Telegram: @xftadmin 4.6 ### HALABTECH 4.6 ### ADYUNLOCKER 4.6',
    t='V5', tool=EXA, conf='CONFIRMED', dists='FRPKING (Distributor, Verified), CLEANUNLOCKER (Distributor), GSMNXT, ADYUNLOCKER, OHIDERAUNLOCKER, GSMNINJA, GSMULTIMATE ...', only='unknown', api='unknown', notes='Same template/roster as xiaomiservicetool.com.')
add(groups=['XIAOMI SERVICE TOOL\xa0(XST)'], entity='XIAOMI SERVICE TOOL (xiaomiservicetool.com)', site='xiaomiservicetool.com', url='https://xiaomiservicetool.com/reseller.php',
    role="'Our Trusted Resellers' (no label)", tier='FLAT', excerpt='### OHIDERAUNLOCKER ### HALABTECH ### GSMNINJA', t='V5', tool=EXA, conf='CONFIRMED',
    dists='FRPKING (Distributor), CLEANUNLOCKER (Distributor), ADYUNLOCKER, OHIDERAUNLOCKER, GSMNINJA, GSMULTIMATE, UNLOCKERHUB, IMEIVESERVER, OFFUNLOCK ...', only='unknown', api='unknown', notes='')
add(groups=['Xiaomi Repair Tool XRT'], entity='Xiaomi Repair Tool (XRT; owner GsmBrand)', site='xiaomirepairtool.com', url='https://xiaomirepairtool.com/reseller.php',
    role="Distributor (Ady Unlocker and Martlobs GSM are 'Exclusive Distributor')", tier='DIST', excerpt='#### Ady Unlocker Exlusive Distributor #### HalabTech Distributor #### Martlobs GSM Exclusive Distributor',
    t='V5', tool=EXA, conf='CONFIRMED', dists='Owner GsmBrand; Exclusive Distributors: Ady Unlocker, Martlobs GSM', only='unknown', api='unknown', notes='')
add(groups=['Galaxy Auth'], entity='Galaxy Auth (galaxy-realme.com)', site='galaxy-realme.com', url='https://www.galaxy-realme.com/',
    role="'Official Partners' - 2nd, after the labelled Official Distributor GSMOnlineServer", tier='DIST',
    excerpt='## 🤝 Official Partners Official Distributor GSMOnlineServer 📞 +91 81090 43638 📱 @gsmonlinserver HalabTech 🌐 server.halabtech.com 📱 @htsupport',
    t='V5', tool=EXA, conf='CONFIRMED', dists='GSMOnlineServer (Official Distributor), GSMFastPro, gsmnkg, Ninja Technologies, GSMToolHub, GSMSEKHAR', only='unknown', api='unknown', notes='')
add(groups=['CP-Tool'], entity='CP Tool (Turkey, +905015450724)', site='cp-tool.com', url='https://cp-tool.com/resellers.php',
    role="'Doğrulanmış Bayi' (verified dealer), spelled 'HALABCTECH'", tier='FLAT', excerpt='##### HALABCTECH Doğrulanmış Bayi Ülke: htsupport HalabTech.official.page https://server.halabtech.com',
    t='V6', tool=EXA, conf='CONFIRMED', dists="'Resmi Ortak' (official partner): FAST PROVISION TEAM, Martlobs GSM; dealers incl. ADY Unlocker, Gsm-T-Tool, HiUnlock, Pro Sefer, Off Unlock", only='unknown', api='unknown',
    notes='Exa agent C1 returned unknown; R7 fetch found the listing.')
add(groups=['Zhizhen Schematics'], entity='Zhizhen Schematics (Shenzhen)', site='zhizhensolutions.com', url='https://zhizhensolutions.com/',
    role="'Our Partners' WORLDWIDE slot whose mail link is Halabtech.cert@gmail.com (partner name not rendered)", tier='DIST',
    excerpt='### Our Partners WORLDWIDE - WhatsApp - Telegram - Dribbble - Mail (Halabtech.cert@gmail.com)', t='V6', tool=EXA, conf='STRONG',
    dists='other partners by country only (Peru, Indonesia, Bangladesh, India, Ethiopia ...); agent saw GSMTIGER, GSMSERVER, AdyUnlocker', only='unknown', api='unknown',
    notes='Identification via HalabTech cert e-mail (also used on smarttool.top and pixelprotool.com). Updates R6 A1 negative (Zhizhen status UNKNOWN).', supports='A1 negative (schematics vendors) updated')
add(groups=['AH-Xiaomi Tool'], entity='AH-COMPANY AUTH TOOL (ah-tool.com)', site='ah-tool.com', url='https://ah-tool.com/',
    role="'Authorized Distributors & Resellers': Halabtech Server - World Wide", tier='DIST', excerpt='### DhiQar Service World Wide ### Halabtech Server World Wide',
    t='V7', tool=EXA, conf='CONFIRMED', dists='adyunlocker (Verified), Aze Gsm (Azerbaijan), DhiQar Service, Muhammad Amin', only='unknown', api="unknown ('Prices update directly from the activation API')", notes='')
add(groups=['HXRU Xiaomi', 'HXRU (OPPO, Realme and OnePlus)'], entity='HXRU AUTH TOOL (hxrutool.net)', site='hxrutool.net', url='https://hxrutool.net/reseller.php',
    role='Main Distributor (ID #14; 5th of 11 Main Distributors)', tier='TOP', excerpt='Main Distributor ID #14 ### HalabTech Verification Verified Partner Contacts 3 Available',
    t='V7', tool=EXA, conf='CONFIRMED', dists='Main: LegitUnlocks, CleanUnlocker, GSM BROTHERS, 3GSM, Kandil-unlocker, GsmUnlockServer, DhiQar-service, Flash Unlock, ContinentalGSM, GSM Friday; Distributors: Adyunlocker, AkUnlocker, FRP King ...', only='unknown', api='unknown', notes='')
add(groups=['MAT AUTH TOOL'], entity='MAT AUTH TOOL (owner mahadev@telecom)', site='matauthtool.com', url='https://matauthtool.com/reseller.php',
    role='Distributor - first entry after the Owner', tier='DIST', excerpt='### mahadev@telecom Owner Verified ### HalabTech Distributor Verified ### SERVER IN-GSM Reseller',
    t='V7', tool=EXA, conf='CONFIRMED', dists='Clean Unlocker, Leope-Gsm, GSMUnlockInfo, Flash Unlock, PowerUnlock, CLickUnlock, offunlock, Martlobs, HNB SOFTWARE, Mubeen (Distributors)', only='unknown',
    api="yes ('Resellers get bulk pricing, sub-account creation, and a dedicated dashboard')", notes='')
add(groups=['Multi Pro TOOL'], entity='MULTIPROTOOL (multiprotool.com)', site='multiprotool.com', url='https://multiprotool.com/resellerlist/',
    role='Worldwide Distributor (Turkey)', tier='DIST', excerpt='#### HALABTECH Worldwide Distributor (Turkey) [WhatsApp](https://server.halabtech.com/contactus)',
    t='FC2', tool=FC, conf='CONFIRMED', dists='FRP KING SERVER, Soul Unlocker, ADY Unlocker, OFFUNLOCK, DhiQar-service, HaymiNet, GOLD UNLOCKER, HI UNLOCK, UNLOCK EASY ... (Worldwide Distributors)', only='unknown', api="panel ('Reseller Login' at multiprotool.com/reseller)", notes='Exa render omitted names; Firecrawl showed them.')
add(groups=['Xiaomi Speed Tool'], entity='Xiaomi Speed Tool Pro (xiaomispeedtoolpro.com)', site='xiaomispeedtoolpro.com', url='https://xiaomispeedtoolpro.com/reseller.php',
    role='Distributor (one of two distributors, after ADMIN)', tier='TOP', excerpt='##### XIAOMI SPEED TOOL PRO ADMIN ##### HEART UNLOCK Distributor ##### HALAB TECH Distributor ##### adyunlocker',
    t='V7', tool=EXA, conf='CONFIRMED', dists='HEART UNLOCK (Distributor), adyunlocker', only='unknown', api='unknown', notes='')
add(groups=['MobileProTool Credit'], entity='MobileProTool (mobileprotool.com)', site='mobileprotool.com', url='https://mobileprotool.com/resellers.php',
    role="the only listed partner ('Remote Wolrdwide')", tier='SOLE', excerpt='Partner Territory Contact Verification HA Halabtech halantech Remote Wolrdwide https://server.halabtech.com/contactus',
    t='V7', tool=EXA, conf='CONFIRMED', dists='none other', only="implied ('Partners handle onboarding, credit delivery, and local support for the tool')", api='unknown', notes='')
add(groups=['Falcon Multi Tool'], entity="FalconMultiTool (falconmultitool.com; 'FalconMultiTool Team' owner)", site='falconmultitool.com', url='https://falconmultitool.com/',
    role='Distributor WorldWide (Main Distributor is GSM Manager)', tier='DIST',
    excerpt='### GSM Manager Main Distributor ### FalconMultiTool Team Owner ### GSMPURE || PUREUNLOCKER Distributor WorldWide ### Halab Tech Distributor WorldWide',
    t='V7', tool=EXA, conf='CONFIRMED', dists='Main Distributor GSM Manager; GSMPURE, dmunlocker, IMEISTAR, FRP King, Mhmd frp', only='unknown', api='unknown', notes='Same owner and roster as opluspro.net.', supports='D-22')
add(groups=['FRP BOSS TOOL'], entity='FRP BOSS TOOL (frpbosstool.com)', site='frpbosstool.com', url='https://frpbosstool.com/seller.php',
    role='Distributor - Worldwide', tier='DIST', excerpt='### HalabTech Distributor - Worldwide Reseller Image', t='V7', tool=EXA, conf='CONFIRMED',
    dists='FRP KING SERVER, Clean Unlocker, R GSM SERVER, ADY Unlocker, Click Unlock, GSM T-TOOL, KSA-UNLOCK, DM UNLOCKER, GSM SERVER, AsUnlocker, Full Unlock MX, GSMFASTEST (Distributor - Worldwide)', only='unknown', api='unknown', notes='')
add(groups=['Anonymous Tool'], entity='Xiaomi Anonymouse Tool (xiaomiauth.net)', site='xiaomiauth.net', url='https://xiaomiauth.net/resellers_and_distributors.php',
    role="Distributor - first row 'HalabTech - Turkey & WorldWide'", tier='DIST', excerpt='| HalabTech - Turkey & WorldWide | Distributor | | Official Site |',
    t='V7', tool=EXA, conf='CONFIRMED', dists='ADY Unlocker, IMEI ve SERVER, OFFUNLOCK, Beeunlock, Cemerkoc, FRP King, Leope-Gsm, OhideraUnlocker, PK GSM, SERVER IN-GSM, TopUnlocksite, Appleunlockers (Distributors)', only='unknown', api='unknown',
    notes='HalabTech SKU cites xiaomiauth.org; partner page is on xiaomiauth.net (same brand). Updates R6 A2 negative (homepage had no list).', supports='A2 negative (Xiaomi Anonymous Tool) updated')
add(groups=['mifrp Tool'], entity='MiFrp (mifrp.com)', site='mifrp.com', url='https://mifrp.com/resellers.php',
    role='◆ Distributor (1 of 6)', tier='DIST', excerpt='HALABTECH ◆ Distributor 💳 Paypal, USDT, Visa And Other payment gateway', t='V7', tool=EXA, conf='CONFIRMED',
    dists='GSM-AFGHAN, AdyUnlocker, kamran_Gsm, MD UNLOCKER, Easy-Unlocker', only='unknown', api='unknown', notes='')
add(groups=['Repair-Fix Xiaomi Auth Tool'], entity='Repair-Fix (repairfixauthtools.com)', site='repairfixauthtools.com', url='https://repairfixauthtools.com/ourreseller.php',
    role="'REPAIRFiX AUTHORIZED RESELLERS' (no label)", tier='FLAT', excerpt='## Adyunlocker WhatsApp: +12816728384 ## HalabTech Telegram: Support HalabTech ## GSMPURE',
    t='V7', tool=EXA, conf='CONFIRMED', dists='Mobile Unlock King (Distributor), FRUNLOCKER (Distributor), Gsmunlockserver, Leope-Gsm ...', only='unknown', api='unknown', notes='HalabTech SKU price $0 at 10:03Z (likely disabled).')
add(groups=['Android Auth Tool Credit'], entity='Android Auth Tool (androidauthtool.com)', site='androidauthtool.com', url='https://androidauthtool.com/reseller.php',
    role="'Authorized Resellers' (no label)", tier='FLAT', excerpt='##### Soso GSM Distributor - Romania , Worldwide ##### Halabtech ##### SERVER IN-GSM',
    t='V7', tool=EXA, conf='CONFIRMED', dists='ADY UNLOCKER (Distributor Worldwide), GSMUnlockInfo, Abdul Salam, Soso GSM, SERVER IN-GSM, Muhammed cantas (Distributors)', only='unknown', api='unknown', notes='')
add(groups=['MR AUTH'], entity='MrAuthTool (mrauthtool.com)', site='mrauthtool.com', url='https://mrauthtool.com/team',
    role='Distributor', tier='DIST', excerpt='##### HalabTech Distributor HalabTech HalabTech @HTSupport', t='V8', tool=EXA, conf='CONFIRMED',
    dists='Gsm Fast Pro, ohidera, GSMNXT.COM (@XFTADMIN), Ady Unlocker, Ra1n Unlocker, Martlobs, AppleUnlockers, GsmGenesis, DhiQar, GSM Credit, GsmNinja, Power Unlock', only='unknown', api='unknown', notes='')
add(groups=['MIFIXPRO'], entity='MiFixPro (mifixpro.com)', site='mifixpro.com', url='https://www.mifixpro.com/resellers',
    role='Distributor', tier='DIST', excerpt='#### HALABTECH About: Halabtech (Distributor) Web: server.halabtech.com Telegram: @htsupport', t='V8', tool=EXA, conf='CONFIRMED',
    dists='Topunlocksite, MARTLOBSGSM, Leope-GSM, ADYUNLOCKER, eSimUNlocker, Fixunlocker, GsmAfrica, 3gsm, PowerUnlock, Cleanunlocker ... (Distributors)', only='unknown', api='unknown', notes='')
add(groups=['Xiaomi Fire Tool XFT'], entity='XiaomiFireTool (xiaomifiretool.com)', site='xiaomifiretool.com', url='https://xiaomifiretool.com/',
    role="'Distributors' (1 of 5)", tier='DIST', excerpt='### 𝐀𝐃𝐘𝐔𝐍𝐋𝐎𝐂𝐊𝐄𝐑 Distributors ### 𝐇𝐀𝐋𝐀𝐁𝐓𝐄𝐂𝐇 Distributors', t='V8', tool=EXA, conf='CONFIRMED',
    dists='GSM CREDIT, GSM GENESIS, ADYUNLOCKER, POWER UNLOCK (Distributors)', only='unknown', api='unknown', notes='')
add(groups=['NEXTG Auth Tool'], entity='NEXTG AUTH TOOL (Ding Electronics, India)', site='nextgauthtool.net', url='https://nextgauthtool.net/reseller.php',
    role="Worldwide Distributor - the only 'Distributor' (all others 'Worldwide Reseller')", tier='SOLE', excerpt='### UNLOCK BAYI Worldwide Reseller Worldwide ### HALABTECH Worldwide Distributor Worldwide',
    t='V8', tool=EXA, conf='CONFIRMED', dists='Admin Ding Electronics; resellers IMEI VS SERVER, UNLOCK BAYI, E-GSM, SMARTBUNLOCK, Martlobs, KGUNLOCKER', only="'All resellers are verified and authorized by NEXTG AUTH TOOL' (agent excerpt)", api='unknown', notes='')
add(groups=['Xiaomi King Tool'], entity='Xiaomi King Tool (xiaomikingtool.com)', site='xiaomikingtool.com', url='https://www.xiaomikingtool.com/resellers.html',
    role="listed in the top ('Distributor') block; field 'Reseller Country: WorldWide'", tier='DIST', excerpt='Company: HALABTECH Telegram: @HTSupport Reseller Country: WorldWide Website: HALABTECH',
    t='V8', tool=EXA, conf='CONFIRMED', dists='Easy-Unlocker (Distributor), GSM AFRICA, 3GSM.RU, GsmGenesis, ADY UNLOCKER, SERVER-GSM.NET ...', only='unknown', api='unknown', notes='')
add(groups=['IPRO Tool Credit'], entity='iPro Auth Tool (iproauthtool.com)', site='iproauthtool.com', url='https://iproauthtool.com/reseller.php',
    role="unnamed 'WorldWide - Reseller' card carrying Telegram @HTSupport (but AsUnlocker's WhatsApp)", tier='RES', excerpt='WorldWide - Reseller Whatsapp: +8801721672766 Telegram: @HTSupport',
    t='V8', tool=EXA, conf='LIKELY', dists='Activation Tools (@ACTSupport), Clean Unlocker, GSM-T-TOOL, Gsm Scene, GSM Paid, GSMFASTEST ... (all Reseller)', only='unknown', api='unknown',
    notes='Ambiguous card (name not rendered; phone belongs to AsUnlocker on other pages). Same template/roster as bmt-pro.com/reseller where HALABTECH is named.')
add(groups=['Pixel Pro Tool Activation'], entity='Pixel Pro Tool (Sonu GSM network)', site='pixelprotool.com', url='https://pixelprotool.com/resellers/',
    role="'HALABTECH Master - Official Global Distributor' (first card)", tier='TOP',
    excerpt='## HALABTECH Master Official Global Distributor [server.halabtech.com](https://server.halabtech.com/) [@HTSupport](https://t.me/HTSupport)',
    t='FC1', tool=FC, conf='CONFIRMED', dists='SONU GSM (Trusted Global Reseller), LOCKBROKEN, iPhoneUnlockFix, GSM Sohaib (Verified Distributor), YangUnlocker, GMS RESELLER', only="yes ('Only use these verified channels for activation and support')", api='unknown', notes='Exa render showed only the notice; Firecrawl rendered the cards.')
add(groups=['Knoxwizard Activation'], entity='Knox Wizard (X-TEK; licence WhatsApp +256783245989)', site='knoxwizard.com', url='https://knoxwizard.com/',
    role='Official Distributor - Distributor / Reseller - Worldwide', tier='DIST', excerpt='HalabTech ▼ 🏷 **Official Distributor** 🌍 🌍 Distributor / Reseller — Worldwide 🌐 [server.halabtech.com]',
    t='FC1', tool=FC, conf='CONFIRMED', dists='Official Distributors: FRP King Server, SUPPORT UNLOCKER, AK GSM ZONE, GSM Africa, HELLO UNLOCKER, Sharafat Gsm, UNLOCK EASY, OrionGsm; many East-African resellers', only='unknown', api='unknown',
    notes='Vendor prices $30/3m, $40/6m, $50/12m vs HalabTech $23.99/$28.99/$39.99 (0.73-0.80 of list).')
add(groups=['Cerberus Tool Pro'], entity='Cerberus Tool (Cerberus Tool Pro / Tool Box)', site='cerberustoolpro.com', url='https://cerberustoolpro.com/partners',
    role='Special Distributor - first of 6 partners (top tier with ADYunlocker and TEAM UNLOCK)', tier='TOP',
    excerpt='6 partners ## HALABTECH Special Distributor [Website](https://server.halabtech.com/) [WhatsApp](https://wa.me/963992951910)', t='FC2', tool=FC, conf='CONFIRMED',
    dists='Special Distributors: ADYunlocker, TEAM UNLOCK; Big Distributor GsmHabib; Distributor bandarula; Reseller gsmmeliodas', only="yes (FAQ: contact a listed Cerberus reseller or distributor)",
    api="yes ('A DHRU-compatible API for your reseller panel'; 'Seller access is enabled on your account by the Cerberus team')",
    notes='Resolves R6 A2 negative (Exa timeout).', supports='A2 negative (Cerberus) resolved')
add(groups=['Alien tool'], entity='Alien Tool (alientool.app; support +55 88 99373-4779)', site='alientool.app', url='https://alientool.app/resellers.html',
    role='Top Reseller - Verified - Worldwide (2nd of 10)', tier='DIST', excerpt='Halabtech Top Reseller Verified Worldwide WhatsApp[963992951910](https://wa.me/963992951910)',
    t='FC3', tool=FC, conf='CONFIRMED', dists='FRP King Server, AmirGsm, FRP Monster, KATTGSM, MartlobsGSM, Ninja Server, Mubeen Unlocker, HELLO-UNLOCKER, GSMELITEFRP (all Top Reseller)', only="yes ('Purchase only through the authorized reseller listed above')", api='unknown', notes='')

TIER_TXT = {
 'SOLE': 'HalabTech is the only (or only distributor-tier) partner the vendor names, so the most plausible route is direct purchase from the developer; no co-listed distributor exists to buy from.',
 'TOP': 'HalabTech sits in the vendor top tier (master/special/main/big/super-premium); direct purchase from the developer is the most plausible route.',
 'TOP4': 'HalabTech is one of the few top-tier World-Wide distributors; direct purchase from the developer is plausible.',
 'DIST': 'HalabTech is one of several listed distributors; direct developer supply is plausible but co-listed distributors are alternative sources.',
 'RES': 'HalabTech is listed only at reseller tier; credits may come via a listed distributor (see distributors) or directly from the vendor.',
 'FLAT': 'Flat list without tiers; HalabTech is an authorised channel but the fulfilment route is not indicated.'}

findings = []
def F(**k):
    k.setdefault('pub_date', ''); k.setdefault('access', 'full page'); k.setdefault('supports_or_contradicts', ''); k.setdefault('notes', '')
    findings.append(k)

for d in L:
    groups = d['groups']
    conf = d['conf']
    role_for = 'Original Developer'
    supply = TIER_TXT[d['tier']]
    api = d['api']
    if api.startswith('yes') and d['tier'] in ('SOLE', 'TOP', 'TOP4', 'DIST', 'RES'):
        supply += ' Vendor runs its own reseller API/panel, so a direct API connection by HalabTech is LIKELY (not proven).'
    vtxt = 'page fetched and HalabTech entry read' if conf == 'CONFIRMED' else 'page fetched; HalabTech identification indirect/ambiguous'
    notes = ('R7 verification: %s (%s, %s). ' % (vtxt, d['tool'].split('__')[-1], T[d['t']])) + \
            'Distributors/co-listed: %s. Sells only via resellers/distributors: %s. Own reseller API/panel: %s. Supply inference: %s %s' % (d['dists'], d['only'], api, supply, d.get('notes', ''))
    TL = {'SOLE': 'sole listed partner', 'TOP': 'top-tier distributor', 'TOP4': 'top-tier World-Wide distributor', 'DIST': 'listed distributor',
          'RES': 'listed reseller (distributor tier held by others)', 'FLAT': 'listed authorised reseller, no tiers'}
    F(entity=d['entity'], entity_website=d['site'], role_for_halabtech=role_for,
      chain_layer='Original Developer -> HalabTech (%s)' % TL[d['tier']],
      direction='%s -> HalabTech' % d['entity'].split(' (')[0],
      halabtech_groups_affected=groups, skus_affected=[],
      claim="%s's official reseller/distributor page lists HalabTech as: %s." % (d['entity'].split(' (')[0], d['role']),
      evidence_type='vendor page', source_url=d['url'], retrieved_utc=T[d['t']], excerpt=d['excerpt'], tool=d['tool'], confidence=conf,
      alternative_explanations='A vendor listing documents an authorised sales channel only; HalabTech may still restock through a co-listed distributor or wholesaler, or the listing may be stale.',
      contradicting_evidence={'CONFIRMED': 'None found on the page.', 'STRONG': 'Partner name not rendered; identification rests on the HalabTech cert e-mail address only.'}.get(conf, 'Card name not rendered; WhatsApp number on the card belongs to AsUnlocker on other vendor pages.'),
      what_would_confirm='Vendor or HalabTech statement that HalabTech orders are fulfilled through the vendor panel/API (e.g. HalabTech SKU names/IDs synchronised from the vendor API).',
      what_would_reject='HalabTech SKUs matching another distributor\'s Dhru catalogue (identical names, IDs and price ratios) or the vendor removing HalabTech.',
      supports_or_contradicts=d.get('supports', ''), notes=notes)

# Octoplus (R6) ----------------------------------------------------------
OCTO = ['Octoplus Box / Dongle (Renew)', 'Octoplus / Octopus Box Credits', 'Octoplus FULL Digital License (Online Without Box)', 'Octoplus/Octopus Activation (Box & Dongle)',
        'Octoplus Samsung Digital License (Online Without Box)', 'Octoplus LG Digital License (Online Without Box)', 'Octoplus FRP Digital License (Online Without Box)', 'Octoplus HUAWEI Digital License (Online Without Box)']
F(entity='Octoplus Box team', entity_website='octoplusbox.com', role_for_halabtech='Original Developer', chain_layer='Original Developer -> HalabTech (official reseller)', direction='Octoplus team -> HalabTech',
  halabtech_groups_affected=OCTO, skus_affected=[], claim='All eight never-checked Octoplus groups belong to the vendor whose Buy Now page lists HALABTECH as an official reseller (worldwide block and Turkey), per R6 A1-10.',
  evidence_type='vendor page', source_url='https://www.octoplusbox.com/ (Buy Now / official resellers; R6 A1-10)', retrieved_utc=T['R6'], excerpt='(see R6 A1-10; not re-fetched in R7)', access='full page (R6)', tool='R6 A1 stream',
  confidence='CONFIRMED', alternative_explanations='Octoplus names no distributor tier; HalabTech could still buy box/dongle credits via a wholesaler.', contradicting_evidence='None.',
  what_would_confirm='Octoplus statement on reseller credit purchasing.', what_would_reject='Octoplus delisting HalabTech.', supports_or_contradicts='A1-10 supported (group mapping added)',
  notes='Group-to-vendor mapping only; no R7 MCP call spent (budget).')

# Inference / family / candidate findings --------------------------------
F(entity='Cerberus Tool (seller dashboard with DHRU-compatible API)', entity_website='cerberustoolpro.com', role_for_halabtech='API Supplier',
  chain_layer='Original Developer/API Supplier (Cerberus) -> HalabTech (Special Distributor) via vendor DHRU API', direction='Cerberus -> HalabTech',
  halabtech_groups_affected=['Cerberus Tool Pro'], skus_affected=['Cerberus Tool box', 'Cerberus Tool bundle', 'Cerberus Tool Pro Activation'],
  claim="Cerberus offers sellers a DHRU-compatible API and lists HalabTech as Special Distributor; HalabTech's 02:00->10:03 rename of its Cerberus SKUs into the vendor's own product names (Tool Box / Bundle / Tool Pro) fits an automatic name-sync from that API.",
  evidence_type='vendor page', source_url='https://cerberustoolpro.com/', retrieved_utc=T['FC1'],
  excerpt='- A DHRU-compatible API for your reseller panel  Seller access is enabled on your account by the Cerberus team.',
  tool=FC, confidence='LIKELY',
  alternative_explanations='HalabTech may have renamed SKUs manually to match the vendor relaunch (Tool Pro + Tool Box + Bundle) without any API link; the partner list only proves a seller account.',
  contradicting_evidence="Prices do not follow one markup: vendor public Tool Pro $50/yr and Tool Box $30/yr vs HalabTech 'Pro Activation' $24.99 and 'Tool box' $39.99 (10:03Z); seller role prices are not public.",
  what_would_confirm='Cerberus API product names/IDs matching HalabTech SKU strings exactly; further renames that track vendor changes within minutes.',
  what_would_reject='HalabTech Cerberus SKUs matching another distributor (ADYunlocker/TEAM UNLOCK) catalogue names and price ratios.',
  supports_or_contradicts='R7 brief Cerberus rename observation supported', notes='Partner directory read via Firecrawl (cerberustoolpro.com/partners, 10:26Z).')

F(entity='SIM-UNLOCKER PRO reseller API', entity_website='sim-unlocker.net', role_for_halabtech='API Supplier', chain_layer='Original Developer (Sim-Unlocker Pro) -> HalabTech (Reseller) via vendor reseller API',
  direction='Sim-Unlocker Pro -> HalabTech', halabtech_groups_affected=['Samsung Sim-Unlocker'],
  skus_affected=['Sim-Unlocker Pro - The Cheapest Samsung Unlock credits New account ANY Quantity', 'Sim-Unlocker Pro - The Cheapest Samsung Unlock credits Refill / ReCharge Old Account ANY Quantity'],
  claim="Sim-Unlocker Pro gives each reseller its own API to create users and add credits and lists HALABTECH as a reseller, so HalabTech's new-account/refill SKUs most plausibly run on the vendor's reseller API.",
  evidence_type='vendor page', source_url='https://www.sim-unlocker.net/reseller', retrieved_utc=T['FC1'],
  excerpt='BE RESELLER BY YOUR OWN API AND SELL CREDITS ### Get Your Own Reseller API Create users / Add credits /', tool=FC, confidence='LIKELY',
  alternative_explanations="HalabTech could buy from a 'Top Reseller' (HaliUnlock, Ady Unlocker, Unlock King, Fast Unlockers) instead of holding its own API.",
  contradicting_evidence='None.', what_would_confirm='Sim-Unlocker reseller panel naming HalabTech as API client.', what_would_reject='HalabTech SKU strings/prices identical to HaliUnlock or ADY Sim-Unlocker listings.',
  notes="HalabTech price $0.81/credit (10:03Z); other Dhru stores sell at $0.808-0.91.")

F(entity='Apizu MDM Tool reseller API', entity_website='apizutool.one', role_for_halabtech='API Supplier', chain_layer='Original Developer (Apizu) -> HalabTech (SUPER PREMIUM) via vendor Reseller API for Dhru',
  direction='Apizu -> HalabTech', halabtech_groups_affected=['Apizu Tool'], skus_affected=[],
  claim='Apizu runs a Reseller API for Dhru Fusion (R6 A2) and places HalabTech in its top SUPER PREMIUM tier, so a direct API link is the most plausible fulfilment route.',
  evidence_type='vendor page', source_url='https://apizutool.one/reseller.php', retrieved_utc=T['V3'], excerpt='### HalabTech SUPER PREMIUM International Hub English', tool=EXA, confidence='LIKELY',
  alternative_explanations='HalabTech may load licences manually from the vendor or via FRP King Server/CleanUnlocker.', contradicting_evidence='None.',
  what_would_confirm='Apizu API product names matching HalabTech SKUs; vendor statement.', what_would_reject='Evidence that HalabTech buys Apizu via another SUPER PREMIUM partner.', supports_or_contradicts='A2 negative (Apizu) updated')

F(entity='AppleUnlockers (Gsm Anik; CF-Tools Main Distributor)', entity_website='appleunlockers.com', role_for_halabtech='Master Distributor',
  chain_layer='CF Tools (ChopelFlasher) -> AppleUnlockers (Main Distributor) -> HalabTech (Worldwide Reseller)', direction='AppleUnlockers -> HalabTech',
  halabtech_groups_affected=['CF-Tools Activation', 'CF-Tools Credit'], skus_affected=[],
  claim="CF Tools names AppleUnlocker as its single Main Distributor and HalabTech as a 'Worldwide Reseller'; with the vendor's Distributor->Reseller DHRU tiering (R6 A2) AppleUnlockers is the most plausible account above HalabTech.",
  evidence_type='vendor page', source_url='https://cftoolsid.com/reseller', retrieved_utc=T['V3'], excerpt='#### AppleUnlocker Main Distributor Reseller Welcome Name: Appleunlockers Website: appleunlockers.com', tool=EXA, confidence='LIKELY',
  alternative_explanations='HalabTech may hold a reseller account created directly by the developer; UnlockerBD and GSMUnlockInfo are also country distributors.',
  contradicting_evidence='None.', what_would_confirm='CF Tools/AppleUnlockers stating HalabTech sits under AppleUnlockers; matching price ratios.', what_would_reject='Developer statement that HalabTech is a direct reseller.',
  notes="Agent B2 also quoted cftoolsid.com/home: 'Reseller system ... Contact our main Distributor.' (agent-only, not re-fetched).")

F(entity='GsmDone.com (Dhru Web API partner of GsmAuth.com)', entity_website='gsmdone.com', role_for_halabtech='API Supplier', chain_layer='GsmAuth.com -> GsmDone.com (Dhru Web API) -> HalabTech',
  direction='GsmDone.com -> HalabTech', halabtech_groups_affected=['Gsm Auth Tool'], skus_affected=['GsmAuth.com QUALCOMM/MEDIATEK Credits Refill | Existing User Only'],
  claim='GsmAuth.com states that GsmDone.com provides the Dhru Web API that other websites use to recharge GsmAuth.com user credits, making GsmDone the most plausible upstream for HalabTech\'s GsmAuth refill SKU.',
  evidence_type='vendor page', source_url='https://www.gsmauth.com/', retrieved_utc=T['V8'],
  excerpt='GsmDone.com Provide Dhru Web API to Other websites For Recharge GsmAuth.com User Account Credits (Auto & instant Service).', tool=EXA, confidence='LIKELY',
  alternative_explanations='GsmAuth (Sohaib Akram, +92 322 4616149) may also sell directly; HalabTech SKU is priced $0 at 10:03Z (probably disabled).', contradicting_evidence='None.',
  what_would_confirm='GsmDone Dhru catalogue entry with the same service name/price basis.', what_would_reject='HalabTech naming another source.')

F(entity='GsmEasy (sole SETool distributor)', entity_website='imei.us / gsmeasy', role_for_halabtech='Master Distributor', chain_layer='SETool team -> GsmEasy (distributor) -> HalabTech', direction='GsmEasy -> HalabTech',
  halabtech_groups_affected=['Setool'], skus_affected=['LG Tool Activation setool', 'LGE Credits 1x100 credits per each', 'LGE Credits [ 1 Packet (x100 credits per each) ] Instant'],
  claim='The official SETool support page names GsmEasy as the only distributor for sales, and HalabTech is not listed, so HalabTech\'s SETool LG activations/credits most plausibly come from GsmEasy or a GsmEasy reseller.',
  evidence_type='vendor page', source_url='https://files.setool.net/support/SETool2/', retrieved_utc=T['V12'],
  excerpt='For sales enquiry please contact with our distributors: GsmEasy, Skype: GsmEasy', tool=EXA, confidence='LIKELY',
  alternative_explanations='The page is the old SETool2 (SonyEricsson) support page and may be outdated for the LG tool; HalabTech could buy from another GsmEasy reseller.',
  contradicting_evidence='None.', what_would_confirm='Current SETool LG distributor list; GsmEasy price parity.', what_would_reject='SETool naming HalabTech or another distributor.',
  supports_or_contradicts='A1 negative (Setool no official list) updated; C-18 (GsmEasy) extended')

F(entity='Ady Unlocker (sole Tira distributor; Fast Unlocker Pro payment contact)', entity_website='adyunlocker.com', role_for_halabtech='Intermediate Supplier',
  chain_layer='Tira / Fast Unlocker Pro -> ADY Unlocker -> HalabTech (candidate)', direction='ADY Unlocker -> HalabTech (candidate)',
  halabtech_groups_affected=['Tira unlocker', 'Fast Unlocker Pro', 'The Magic Tool', 'Guerratool MOTO'], skus_affected=[],
  claim="ADY Unlocker is Tira's only listed distributor (HalabTech is reseller-tier), receives Fast Unlocker Pro's direct crypto payments on WhatsApp +12816728384, and is the only worldwide reseller on TheMagicTool/GuerraTool where HalabTech is absent - making ADY a candidate upstream for these groups.",
  evidence_type='vendor page', source_url='https://fast-unlocker-pro.com/', retrieved_utc=T['V1'], excerpt='After Payment Send (Payment ScreenShot) to | WhatsApp, +12816728384 telegram', tool=EXA, confidence='UNKNOWN',
  alternative_explanations='Tira and Fast Unlocker Pro may supply HalabTech directly (HalabTech is itself a Fast Unlocker Pro distributor); ADY is simply the largest co-distributor across many vendors.',
  contradicting_evidence='HalabTech is listed as a distributor on fast-unlocker-pro.com, which argues for a direct account there.',
  what_would_confirm="ADY Dhru catalogue entries with HalabTech-identical SKU strings/prices for Tira, Magic Tool, GuerraTool.", what_would_reject='Vendor statements that HalabTech buys direct.',
  notes='+12816728384 is shown as ADY Unlocker WhatsApp on smarttool.top, tera-tool.com, motokingprotool.com, kgfixtool.com and general-unlocker.com.')

F(entity='GSM Manager (Main Distributor of OPlusPro and FalconMultiTool)', entity_website='gsmmanager.com', role_for_halabtech='Reseller (peer)',
  chain_layer='FalconMultiTool Team -> GSM Manager (Main Distributor) / HalabTech (Distributor WorldWide)', direction='unclear (GSM Manager <-> HalabTech)',
  halabtech_groups_affected=['OPlusProLogin', 'Falcon Multi Tool'], skus_affected=[],
  claim="opluspro.net and falconmultitool.com show the same owner ('FalconMultiTool Team') and the same Main Distributor (GSM Manager), with HalabTech as a separate 'Distributor WorldWide'; GSM Manager is also a HalabTech credit buyer (R6 D-22), so the two are peers rather than a proven chain.",
  evidence_type='vendor page', source_url='https://opluspro.net/', retrieved_utc=T['V2'], excerpt='### GSM Manager Main Distributor ### FalconMultiTool Team Owner', tool=EXA, confidence='UNKNOWN',
  alternative_explanations='HalabTech, being a listed distributor, most plausibly buys direct from FalconMultiTool Team.', contradicting_evidence='R6 D-22: GSM Manager resells HalabTech credits (opposite direction).',
  what_would_confirm='SKU-string/price parity between GSM Manager and HalabTech OPlusPro SKUs.', what_would_reject='Vendor statement of direct supply.', supports_or_contradicts='D-22 context')

F(entity='Smartbe Unlock (Mysterio FRP primary wholesale distributor with direct API)', entity_website='smartbeunlock.com', role_for_halabtech='Intermediate Supplier',
  chain_layer='Mysterio FRP -> Smartbe Unlock / Clean Unlocker Team -> HalabTech (candidate)', direction='Smartbe Unlock -> HalabTech (candidate)',
  halabtech_groups_affected=['Mysterio FRP'], skus_affected=['Mysterio FRP Unlock Refill (Old User) [AUTO API]'],
  claim='Mysterio FRP does not list HalabTech; it names Smartbe Unlock as its primary wholesale distributor with direct API access (plus Clean Unlocker Team), so HalabTech\'s [AUTO API] Mysterio SKU likely comes through one of them or an unlisted API account.',
  evidence_type='vendor page', source_url='https://www.mysteriofrp.com/', retrieved_utc=T['V5'],
  excerpt='Our primary wholesale distributor with the widest coverage and direct API access for instant, fully-automated services.', tool=EXA, confidence='UNKNOWN',
  alternative_explanations="Mysterio sells an 'API integration' tier to platforms; HalabTech could hold it without being listed.", contradicting_evidence='None.',
  what_would_confirm='Smartbe/Clean Unlocker catalogue with HalabTech-identical SKU wording and price ratio.', what_would_reject='HalabTech shown on a Mysterio list.')

F(entity='Tool family: Yemeni Samsung/LG unlock tools (Hali-Unlock network)', entity_website='general-unlocker.com; tiraunlocker.com; fast-unlocker-pro.com; uft-tool.com; sim-unlocker.net; haliunlock.com; oneclick-tool.com',
  role_for_halabtech='Master Distributor', chain_layer='Yemeni developers -> {Hali Unlock, Speed Unlocker, All Unlocker, ADY Unlocker, GSM-T-TOOL} distributor tier -> HalabTech (distributor/reseller)',
  direction='family -> HalabTech', halabtech_groups_affected=['General Unlocker Pro', 'Tira unlocker', 'Fast Unlocker Pro', 'UFT-Tool', 'Samsung Sim-Unlocker', 'Alseery Unlocker', 'Golden-Unlocker', 'QCDMA Tool', 'ONE CLICK PhoneRepair'],
  skus_affected=[],
  claim='Reachable Yemeni-linked tools (General Unlocker, Tira, Fast Unlocker Pro, UFT-Tool, plus Sim-Unlocker Pro via Top Reseller HaliUnlock) share one distribution network - Hali Unlock, Speed Unlocker, All Unlocker, ADY Unlocker, GSM-T-TOOL - and every rendered list includes HalabTech; HaliUnlock itself (search snippet) sells Global Unlocker Pro, Sim-Unlocker Pro, General Unlocker Pro, QCDMA TOOL and CDMA YEMEN TOOL.',
  evidence_type='distributor directory', source_url='https://general-unlocker.com/reseller/', retrieved_utc=T['V1'],
  excerpt='هالي سلاح المهندسين haliunlock WorldWide distributor Main Distributor / Ask to be a Distributor WorldWide - Yemen - Arabic Countries', tool=EXA, confidence='LIKELY',
  alternative_explanations='Shared distributor names reflect a regional market, not a shared back office; HalabTech can hold direct accounts with each developer.',
  contradicting_evidence='Tira names only ADY as distributor (not Hali); Sim-Unlocker Pro is run from Pakistan (+923002525532). Alseery and Golden-Unlocker sites are parked/suspended.',
  what_would_confirm='Common panel software/API host for these tools; Hali Unlock catalogue strings identical to HalabTech SKUs ([ Samsung + LG + Alcatel + TINNO + Google + Moto ] ... [ Auto API ]).',
  what_would_reject='Each developer confirming direct HalabTech accounts.', supports_or_contradicts='A2-07, A2-10, A2-14, A2-15 (Global Unlocker/KEY-Tool/Hunter/Q-Unlocker) extended; D-16 lead (CDMA Yemen Tool sold by HaliUnlock)',
  notes="General Unlocker (Al Qasr Street, Sanaa) and OneClick Tool ('اليمن، صنعاء، شارع القصر', +967773355567) share a street address. All Unlocker phone +962789940944 appears on general-unlocker.com and with info@halabtech.com on global-unlocker-pro.com (R6 A2 anomaly).")

F(entity='Tool family: Indian OTP/auth tools (RFT Loader + GSM Future Tool template)', entity_website='rftloader.com; gsmfuture.in; nexapro.co.in; galaxy-realme.com; smartfrptool.com',
  role_for_halabtech='Original Developer', chain_layer='Indian developer(s) -> {Softsoln, Gsmninja, Halabtech, Adyunlocker} World-Wide distributors', direction='family -> HalabTech',
  halabtech_groups_affected=['RFT Loader', 'Gsm Future Tool', 'Nexa Pro Tool', 'Galaxy Auth', 'Smart Frp Tool', 'Lazy Loader'], skus_affected=[],
  claim='rftloader.com and gsmfuture.in use the same reseller-page template and wording and the same four top distributors (Softsoln, Gsmninja, Halabtech, Adyunlocker), indicating one developer/back office; Nexa Pro, Galaxy Auth and Smart FRP share the Indian distributor pool and also list HalabTech (Lazy Loader does not).',
  evidence_type='public JS/HTML', source_url='https://gsmfuture.in/resellers.php', retrieved_utc=T['V4'],
  excerpt='Important — Buy Only from Official Resellers Listed Below Always purchase GFT OTPs from the official resellers listed on this page only.', tool=EXA, confidence='LIKELY',
  alternative_explanations='A shared website template can be bought from the same web developer by unrelated tool owners.', contradicting_evidence='None.',
  what_would_confirm='Shared hosting/admin contact or identical OTP back-end host.', what_would_reject='Different owners stated on the sites.', supports_or_contradicts='C-11 related')

F(entity='Tool family: Tanzanian MDM tools (360 TOOL / HSPRO TOOL template; Apizu, Knox Wizard, SmartTool Pro network)', entity_website='tojo360.com; hijatekunloker.com; apizutool.one; knoxwizard.com; smarttool.top; robytechtool.com',
  role_for_halabtech='Original Developer', chain_layer='East-African developers -> {FRP King Server, UnlockerBD, Ohidera, HalabTech ...}', direction='family -> HalabTech',
  halabtech_groups_affected=['tojo360 Tool', 'HSPRO TOOL Activation', 'Apizu Tool', 'Knoxwizard Activation', 'Smart Tool Pro Tool', 'Robytechtool'], skus_affected=[],
  claim='tojo360.com and hijatekunloker.com carry identical feature blocks and near-identical reseller rosters (FRP King Server, HalabTech, UnlockerBD, Ohideraunlocker, GMS RESELLER) and list HalabTech as Worldwide Distributor; Apizu, Knox Wizard and SmartTool Pro share the East-African reseller pool and list HalabTech, while Roby Tech Tool (same pool) omits it.',
  evidence_type='public JS/HTML', source_url='https://hijatekunloker.com/', retrieved_utc=T['V3'],
  excerpt='Tecno/Infinix/Itel MTK SEC 6/2024 MDM bypass no relock #### Samsung MDM 2025 bypass with KG active/broken/error support', tool=EXA, confidence='LIKELY',
  alternative_explanations='Template reuse by separate Tanzanian developers; shared rosters reflect common wholesalers.', contradicting_evidence='Roby Tech Tool omits HalabTech.',
  what_would_confirm='Same admin contact/hosting; same server back end.', what_would_reject='Distinct owners and servers.')

F(entity='Tool family: Bangladeshi FRP-King/Clean-Unlocker template (Falcon FRP Tool, Xiaomi Service Tool) and GSMNXT (@XFTADMIN)', entity_website='falconfrptool.com; xiaomiservicetool.com; mrauthtool.com; fastfrptool.com; xiaomifiretool.com',
  role_for_halabtech='Original Developer', chain_layer='developers -> FRPKING/CLEANUNLOCKER (Distributors) + HalabTech', direction='family -> HalabTech',
  halabtech_groups_affected=['Falcon FRP Tool', 'XIAOMI SERVICE TOOL\xa0(XST)', 'MR AUTH', 'FAST FRP TOOL', 'Xiaomi Fire Tool XFT'], skus_affected=[],
  claim='falconfrptool.com and xiaomiservicetool.com share one reseller-page template with FRPKING and CLEANUNLOCKER as the only labelled Distributors and HalabTech listed; GSMNXT (Telegram @XFTADMIN) is a distributor on Falcon FRP, Fast FRP Tool and MR AUTH, pointing to an XiaomiFireTool-linked Indian admin.',
  evidence_type='public JS/HTML', source_url='https://falconfrptool.com/reseller.php', retrieved_utc=T['V5'], excerpt='### FRPKING Distributor Verified Bangladesh/Worldwide Telegram: @frpkingaksumon 4.8 ### CLEANUNLOCKER Distributor', tool=EXA, confidence='UNKNOWN',
  alternative_explanations='Same web template sold to several tool owners.', contradicting_evidence='None.', what_would_confirm='Shared admin/back-end.', what_would_reject='Distinct owners.')

F(entity='Tool family: Dhru-API white-label auth panel (Venom Auth Tool = Ultra Auth Tool template)', entity_website='venomauthtool.com; ultraauth.org', role_for_halabtech='API Supplier',
  chain_layer='white-label auth platform -> Dhru Fusion credit-transfer API -> resellers (HalabTech candidate)', direction='vendor API -> HalabTech (candidate)',
  halabtech_groups_affected=['Venom Auth Tool Credit', 'Ultra auth Tool'], skus_affected=['Venom Auth Tool Credit Any Qnt [OLD/EXISITNG USER]', 'Ultra auth Tool (UAT) QC/ MTK/ FDL Credits refill [Existing User]'],
  claim="venomauthtool.com and ultraauth.org are the same white-label site (identical copy) and both advertise a 'Dhru Fusion-compatible API for resellers to transfer credits'; their reseller lists are empty, so HalabTech's credit SKUs most plausibly use that vendor API.",
  evidence_type='public JS/HTML', source_url='https://www.venomauthtool.com/', retrieved_utc=T['V8'], excerpt='Credit Transfer API Dhru Fusion-compatible API for resellers to transfer credits and manage orders. Dhru API Reseller', tool=EXA, confidence='LIKELY',
  alternative_explanations='HalabTech may buy Venom/Ultra credits from another Dhru store connected to the same API.', contradicting_evidence='No list names HalabTech.',
  what_would_confirm='Vendor reseller list naming HalabTech.', what_would_reject='HalabTech SKU strings matching a third-party store.', notes="Markup forensics: Venom implied upstream cost $0.70 at x1.25 (markup_server.json).")

F(entity='Tool family: reseller-panel template (Eagle Multi Tool = Xiaomi Paid Tool)', entity_website='eaglemultitool.com; xiaomipaid.com', role_for_halabtech='Original Developer',
  chain_layer='white-label Realme authentication/reseller panel', direction='family -> HalabTech', halabtech_groups_affected=['Eagle Multi Tool', 'Xiaomi Paid Tool'], skus_affected=[],
  claim="eaglemultitool.com and xiaomipaid.com use the same panel template ('Realme Authentication Panel ... dedicated reseller panel'; 'Trusted partners worldwide providing ... services and support'); HalabTech is a Distributor of Eagle Multi Tool but absent from Xiaomi Paid Tool, whose owner number 09987753592 matches GSM Paid.",
  evidence_type='public JS/HTML', source_url='https://xiaomipaid.com/', retrieved_utc=T['V8'], excerpt='Login or register to access full Realme authentication, FRP bypass, demo lock removal, and bootloader services through our dedicated reseller panel.', tool=EXA, confidence='UNKNOWN',
  alternative_explanations='Commercial template shared by unrelated owners.', contradicting_evidence='Different owners/rosters.', what_would_confirm='Shared back end.', what_would_reject='Distinct servers.')

F(entity='Tool family: Brazil-linked template (Tuna Pro Tool, FRP Unlock Tool, Penguine Multi Tool, MIFRPTOOL.COM)', entity_website='tunaprotool.com; frpunlocktool.com; penguintool.com; mifrptool.com',
  role_for_halabtech='Not linked', chain_layer='owner/main distributor (supremegsm / FRP BRASIL / Activeunlocker) -> resellers', direction='family -> HalabTech (route unknown)',
  halabtech_groups_affected=['Tuna Pro Tool', 'FRP Unlock TOOL', 'PENGUINE MULTI TOOL', 'MIFRPTOOL.COM'], skus_affected=[],
  claim="These four sites share the same template ('Ultimate Solution for Android Repairing', 'Reseller Login', 'Main distributor') and Tuna's reseller supremegsm uses support@frpunlocktool.com; none of the readable lists includes HalabTech.",
  evidence_type='public JS/HTML', source_url='https://tunaprotool.com/', retrieved_utc=T['V6'], excerpt='#### supremegsm BRASIL & WORLDWIDE - support@frpunlocktool.com - Telegram Channel - Reseller Login', tool=EXA, confidence='UNKNOWN',
  alternative_explanations='Template reuse only.', contradicting_evidence='None.', what_would_confirm='HalabTech SKU parity with supremegsm/FRP BRASIL catalogue.', what_would_reject='Vendor list naming HalabTech.')

F(entity='Tool family: TheMagicTool = GuerraTool (Motorola) template', entity_website='themagictool.net; guerratool.com', role_for_halabtech='Not linked', chain_layer='developer -> ADY UNLOCKER/GUERRADONE/MENDOZA GSM -> ?',
  direction='family -> HalabTech (route unknown)', halabtech_groups_affected=['The Magic Tool', 'Guerratool MOTO'], skus_affected=[],
  claim='Both sites share the same template and reseller names (ADY UNLOCKER, MENDOZA GSM, GUERRADONE); HalabTech is absent from both, so HalabTech\'s Magic/Guerra credit SKUs must come through a listed reseller (ADY Unlocker is the only worldwide one) or an unlisted account.',
  evidence_type='vendor page', source_url='https://guerratool.com/resellers', retrieved_utc=T['V6'], excerpt='## RESELLERS ### ADY UNLOCKER WORD ### MARTLOBS GSM PERU ### LEOPE-GSM PERÚ', tool=EXA, confidence='UNKNOWN',
  alternative_explanations='Lists may be incomplete.', contradicting_evidence='None.', what_would_confirm='ADY catalogue parity.', what_would_reject='Vendor naming HalabTech.')

F(entity='Tool family: BMT Pro = iPro Auth Tool reseller-page template', entity_website='bmt-pro.com; iproauthtool.com', role_for_halabtech='Original Developer', chain_layer='same back office (likely) -> listed resellers incl. HalabTech',
  direction='family -> HalabTech', halabtech_groups_affected=['BMT Pro Tool', 'IPRO Tool Credit'], skus_affected=[],
  claim="bmt-pro.com/reseller and iproauthtool.com/reseller.php show the same card layout and roster (Clean Unlocker, GSM-T-TOOL 'Irak - Reseller', Gsm Scene, GSM Paid, GSMFASTEST, Habesha, UnlockerBD, IDUnlocker +8618652839159); HalabTech is named on BMT and implied (@HTSupport) on iPro.",
  evidence_type='public JS/HTML', source_url='https://iproauthtool.com/reseller.php', retrieved_utc=T['V8'], excerpt='##### GSM-T-TOOL Irak - Reseller Whatsapp: +9647708689458 ##### Gsm Scene Pakistan - Reseller', tool=EXA, confidence='LIKELY',
  alternative_explanations='Same web developer, different owners.', contradicting_evidence='None.', what_would_confirm='Shared owner contact.', what_would_reject='Distinct owners.')

F(entity='Tool family: Turkish partner network (CheckerTR PRO, RADEX, MIUI Tool, CP Tool, E-GSM, Xiaomi Anonymouse, NEXTG)', entity_website='checkertr.com; radexfrp.com; miuitool.com; cp-tool.com; egsmpro.com',
  role_for_halabtech='Original Developer', chain_layer='Turkish developers -> {VIP Pro Support, Dost Service, IMEI ve SERVER, Unlock Bayi, OFFUNLOCK} + HalabTech', direction='family -> HalabTech',
  halabtech_groups_affected=['CheckerTR PRO', 'RADEX FRP TOOL', 'MIUI Tool', 'CP-Tool', 'E-GSM', 'Anonymous Tool', 'NEXTG Auth Tool'], skus_affected=[],
  claim='These vendors share Turkish channel partners (Dost Service, IMEI ve SERVER, Unlock Bayi, UNLOCKERGROUP, OFFUNLOCK, Pro Sefer, HiUnlock); HalabTech is listed on CheckerTR (main distributor), RADEX, CP Tool, E-GSM, Anonymous and NEXTG but not on MIUI Tool (Dost Service + IMEI ve SERVER only).',
  evidence_type='distributor directory', source_url='https://miuitool.com/resellers.php', retrieved_utc=T['V8'], excerpt='# Resellers Official reseller partners. Dost Service https://dostservice.com/ IMEI ve SERVER https://imeiveserver.com', tool=EXA, confidence='UNKNOWN',
  alternative_explanations='Regional overlap only.', contradicting_evidence='None.', what_would_confirm='Common owner.', what_would_reject='n/a',
  notes='MIUI Tool: candidate upstreams Dost Service (also RADEX distributor) or IMEI ve SERVER.')

F(entity="Tool family hypothesis: Thai tools (RTC Tool, MTK GoGo, SimTool, GSMunlock, Artemis II)", entity_website='rtc-tool.com; mtkgogo.com; simtool.net; gsmunlock.net; artemis2.vip', role_for_halabtech='Original Developer',
  chain_layer='untested', direction='n/a', halabtech_groups_affected=['MTK GOGO Tool', 'SimTool', 'GSMunlock', 'Artemis Tool'], skus_affected=['MTK GoGo Create New User + Credits(Instant/Auto API)', 'SIMTool - Create New User + Credits(Instant/Auto API)', 'GSMUnlock- Create New Account (Instant/Auto API)'],
  claim="No shared Thai back office could be shown: mtkgogo.com does not resolve, simtool.net now hosts an unrelated Chinese site, gsmunlock.net is a Tajik GSM store, and Artemis II's Thai site has no list; the 'Create New User + Credits (Instant/Auto API)' wording is a widely copied Dhru string first seen on GSM-Forum from Best4unlock (2022-11-12).",
  evidence_type='forum', source_url='https://forum.gsmhosting.com/vbb/f1116/mtkgogo-a12-unlock-tool-create-new-user-credits-3092737/', retrieved_utc=T['S'], excerpt='MTKGoGo A12 Unlock Tool Create New User + Credits (Instant/Auto API)', access='search snippet', tool='mcp__Exa__web_search_exa', confidence='UNKNOWN',
  alternative_explanations='Thai hypothesis may still hold for RTC (Thai site, HalabTech Distributor WorldWide per R6 A2-17) and Artemis II (Thai-language site).', contradicting_evidence='None.',
  what_would_confirm='Archived mtkgogo.com/simtool.net reseller pages (Wayback) naming the same team.', what_would_reject='Different developers in archives.', supports_or_contradicts='A2-17 context; B-07/B-08 (Best4unlock) linked')

F(entity='HalabTech price position vs vendor list prices (9 vendors)', entity_website='various', role_for_halabtech='Original Developer', chain_layer='vendor list price vs HalabTech guest price', direction='vendor/distributor -> HalabTech',
  halabtech_groups_affected=['UFT-Tool', 'Knoxwizard Activation', 'MultiUnlock Service Utility Tool', 'Fenix Utility Pro', 'Global Frp Tool (GFT)', 'Pixel Service Tool', 'ONE CLICK PhoneRepair', 'tool.emmc-ufs', 'Robytechtool'], skus_affected=[],
  claim='HalabTech guest prices sit at or below the vendors\' own list prices (ratio HalabTech/vendor: UFT 0.96-0.98; Knox Wizard 0.73-0.80; MultiUnlock 0.67-0.79; Fenix 0.88; GFT credit ~1.00; Pixel Service Tool 0.79; OneClick 0.83; emmc-ufs 0.97-1.00; Roby 0.96-1.00), so HalabTech must buy at distributor/reseller discounts.',
  evidence_type='price fingerprint', source_url='https://knoxwizard.com/', retrieved_utc=T['FC1'], excerpt='3 Months $30 one-time payment - Full bypass access - All device brands', tool=FC, confidence='LIKELY',
  alternative_explanations='Vendor list prices may be stale, or HalabTech may run some SKUs at a loss/promotion.', contradicting_evidence='Cerberus Tool box ($39.99) is above vendor list ($30).',
  what_would_confirm='Vendor distributor price sheets.', what_would_reject='HalabTech buying at retail.',
  notes='HalabTech prices from server_catalog_1003.json (10:03Z); vendor prices from R7 fetches 10:17-10:28Z (UFT, Knox, MultiUnlock, Fenix, GFT, PixelService, OneClick, emmc-ufs, Roby).')

F(entity='HalabTech top-tier vendor relationships (direct-supply candidates)', entity_website='various', role_for_halabtech='Original Developer', chain_layer='Original Developer -> HalabTech (top tier)', direction='developers -> HalabTech',
  halabtech_groups_affected=['Cerberus Tool Pro', 'Pixel Pro Tool Activation', 'Eagle Frp', 'TMT Pro Tool', 'NEXTG Auth Tool', 'HXRU Xiaomi', 'HXRU (OPPO, Realme and OnePlus)', 'UNLOCK SERVICE TOOL ( UST )', 'MobileProTool Credit', 'Apizu Tool', 'CheckerTR PRO', 'Xiaomi Speed Tool'], skus_affected=[],
  claim='For 11 vendors HalabTech is the sole partner or in the top tier (Special/Master/Big/Main/SUPER PREMIUM distributor), making direct developer supply (often via vendor API/panel) the most plausible fulfilment route for these groups.',
  evidence_type='vendor page', source_url='https://tmtprotool.com/reseller.php', retrieved_utc=T['V3'], excerpt='#### Big Distributors 1 ###### Halab Tech Big Distributor Worldwide @htsupport', tool=EXA, confidence='LIKELY',
  alternative_explanations='Top-tier labels are marketing; HalabTech may still restock some items through peers.', contradicting_evidence='None.',
  what_would_confirm='API/panel evidence per vendor (as for Cerberus).', what_would_reject='SKU parity with another distributor.')

# ---------------------------------------------------------------- negative findings
NEG = []
def N(group, entity, url, checked, result, tool):
    NEG.append(dict(entity='%s [HalabTech group: %s]' % (entity, group), url=url, what_was_checked=checked, result=result, tool=tool))

AG = 'mcp__Exa__agent_run'
# verified absent
N('Mysterio FRP', 'Mysterio FRP', 'https://www.mysteriofrp.com/', 'official distributor section (live fetch 10:21Z)', "HalabTech ABSENT. Smartbe Unlock = 'Official' primary wholesale distributor with direct API; Distributor Clean Unlocker Team; Reseller OHIDERA UNLOCKER. Vendor sells distributor tiers ($500 deposit), reseller panel and API integration (see candidate finding).", EXA)
N('WorldLinkGSM Tool', 'WorldlinkGSM PRO', 'https://www.worldlinkgsmpro.com/', 'Official Distributors section', "HalabTech not listed: 'No authorized distributors listed yet.' (no list at all).", EXA)
N('Robytechtool', 'ROBY TECH TOOL', 'https://www.robytechtool.com/', "'Our Official Resellers' list", 'HalabTech ABSENT. Resellers: DFM TECH MOBILE, KONGWETECH, Johnny Msk, SAKI MOBILE SHOP, BarikiX, robytechreseller, Bhachu Prem, Dollar254 (East-African). Vendor prices 5/30/50 USDT; HalabTech $4.99/$28.99/$47.99.', EXA)
N('The Magic Tool', 'TheMagicTool', 'https://themagictool.net/resellers', 'RESELLERS list', 'HalabTech ABSENT. ADY UNLOCKER (Worldwide), GSMSERVER (Hong Kong), GUERRADONE, MENDOZA GSM, FULL GSM UNLOCK, DT-UNLOCK, FREDDY ORTIZ.', EXA)
N('Guerratool MOTO', 'GuerraTool', 'https://guerratool.com/resellers', 'RESELLERS list', 'HalabTech ABSENT. ADY UNLOCKER, MARTLOBS GSM, LEOPE-GSM, MENDOZA GSM, GUERRA DONE.', EXA)
N('IMFC', 'iMFC / MFC (mfcbox.com)', 'https://www.mfcbox.com/dealers/', 'Dealers page (Distributor + Reseller sections)', "HalabTech ABSENT. Distributors EOEM CO.,LTD, GSM-SOURCES, ARTGSM, GSMSERVER; ~20 resellers (SIMSIM, MARTVIEW, SHARKGSM ...). 'If the buying not from our dealer will assume the risk of non-warranty'. Candidate upstreams: GsmServer / GSM-Sources.", EXA)
N('FCL Schematic', 'Wuxinji (WXJ) FCL', 'https://wuxinji.com/sub-en4/Buy.html', 'official Buy page', 'HalabTech ABSENT. Only Wuxinji Global/Vietnam/India (zsmalikteam)/Bangladesh/Iraq (golden-iraq)/Indonesia/Malaysia channels.', EXA)
N('ZXW Schematic', 'ZXW (Zillion x Work)', 'https://zxwtools.com/en/buy.html', 'sales agent list', "HalabTech ABSENT. Agents: HAOFANG COMMUNICATION and GSM-Sources (Distributor); 'If you purchase ZXW dongle and software at an unofficial agent, we will not offer any upgrades.' Candidate upstream GSM-Sources (C-19).", EXA)
N('KRAKEN AUTH', 'KrakenAuth', 'https://krakenauthtool.org/buy.php', "'Our Resellers' (4 partners)", 'HalabTech ABSENT. Kibe_r007 (Big Distributor, Istanbul), Soul Unlocker (Big Distributor, soulunlocker.com), Unlockgo.uz (Owner), FixPhone.', EXA)
N('Easy Auth Tool', 'Easy Auth Tool', 'https://easyauthtool.com/', "'Authorized Partners' Distributors", 'HalabTech ABSENT. Distributors: Easy Admin, HEART UNLOCK. Vendor also sells credits directly.', EXA)
N('Tuna Pro Tool', 'Tuna Pro Tool', 'https://tunaprotool.com/', "'Authorized Resellers'", 'HalabTech ABSENT. FRP BRASIL (Worldwide Distributor), supremegsm (support@frpunlocktool.com, Reseller Login).', EXA)
N('XIAOMI FLASHER PRO', 'Xiaomi Flasher Pro (XFP)', 'https://xiaomiflasherpro.com/', "'Authorized Resellers'", 'HalabTech ABSENT. Sole distributor 3gsm.ru (Russia / Worldwide) - candidate upstream.', EXA)
N('MIUI Tool', 'MIUI Tool', 'https://miuitool.com/resellers.php', 'Resellers page', 'HalabTech ABSENT. Only Dost Service and IMEI ve SERVER (Turkey).', EXA)
N('Lazy Loader', 'LazyLoader', 'https://home.lazyloader.in/', "'Authorized Resellers'", 'HalabTech ABSENT. 15 mainly Indian resellers (Gsm Patna, AKUNLOCKER, GsmNinja, HXRU GSM, GSM-T-TOOL, IMEISTAR ...).', EXA)
N('TONI PRO TOOL', 'TONI PRO TOOL', 'https://toniprotool.com/', "'Authorized Distributor/Reseller'", 'HalabTech ABSENT. TONI SARVICE (Owner), akgsmserver, Leope-Gsm, Soso GSM, cleanunlocker, gsm paid, MUBEENUNLOCKER, Arya_Lu, GSMUNLOCK SARVICE, gms reseller.', EXA)
N('Xiaomi Paid Tool', 'Xiaomi Paid Tool', 'https://xiaomipaid.com/', "'Authorized Distributors'", 'HalabTech ABSENT. Owner Ashik khan (09987753592 = GSM Paid number), iphoneunlockingstore, Offlock, ohideraunlocker, AminKhan, Ra1nunlocker, GMTXIAOMI.', EXA)
N('MIFRPTOOL.COM', 'MIFRPTOOL.COM', 'https://mifrptool.com/', "'Authorized Resellers'", "HalabTech ABSENT. Only 'MIFRPTOOL Main Distributor Tool Onwer' shown (sells via owner).", EXA)
N('FRP Unlock TOOL', 'FRP Unlock Tool (Mi FRP Unlock Server)', 'https://frpunlocktool.com/', "'Authorized Resellers'", "HalabTech ABSENT. Only '★ Main distributor' (frpunlocktoolofficial@gmail.com, Reseller Login). Same template as Tuna Pro Tool.", EXA)
N('Typhon Auth Tool', 'Typhon Tool', 'https://typhontool.com/resellers', 'Global Reseller Network directory', "No list: 'No resellers found'. HalabTech status UNKNOWN.", EXA)
N('Setool', 'SETool team', 'https://files.setool.net/support/SETool2/', 'official support page sales contacts', 'HalabTech ABSENT. Only distributor: GsmEasy (see candidate finding).', EXA)
# unreachable
N('king Tools', 'KingTools / KingUnlock', 'https://kingunlock.net/resellerlist.html', 'reseller list', 'UNREACHABLE: Firecrawl DNS resolution failed; Exa CRAWL_UNKNOWN_ERROR. Agent A saw homepage text API Access Instant Sell. UNKNOWN.', FC)
N('T-Unlock', 'T-Unlock', 'https://t-unlock.com/resellers/', 'reseller list', 'UNREACHABLE: DNS resolution failed (Firecrawl), Exa crawl error. UNKNOWN.', FC)
N('MTK GOGO Tool', 'MTK GoGo', 'https://mtkgogo.com/', 'homepage/resellers', 'UNREACHABLE: DNS resolution failed (Firecrawl); Exa crawl error. Dhru stores reference mtkgogo.com/supported-models. UNKNOWN.', FC)
N('Golden-Unlocker', 'Golden-Unlocker', 'https://www.golden-unlocker.com/', 'homepage', "Account suspended ('This Account has been suspended.' - agent A; Tracxn snippet shows suspendedpage.cgi). UNKNOWN.", AG)
N('Alseery Unlocker', 'AlseerY Unlocker (Yemen)', 'https://alseery-unlocker.com/resellers', 'reseller page', "Parked domain (agent A). UNKNOWN. 'Alseery SofT Yemen' appears as a reseller on tiraunlocker.com; halabtech.com hosts AlseerY Unlocker download posts.", AG)
N('SimTool', 'SIMTool.NET', 'https://simtool.net/', 'homepage', 'Domain now serves an unrelated Chinese ceramic-tile site (fetched 10:26Z); official Telegram t.me/simtool per agent A. UNKNOWN.', EXA)
N('Ultra-Unlock Pro', 'Ultra-Unlock Pro', 'https://ultra-unlock.pro/', 'homepage', 'Parked landing page (agent A). UNKNOWN.', AG)
N('GAPro Tool', 'GA Pro Login Tool', 'https://www.gaprologin.com/resellers', 'reseller page', 'Exa HTTP 502; Firecrawl all engines failed. Homepage identifies GA Pro Login Tool (agent D1). UNKNOWN.', FC)
N('Moto M Tool', 'Moto M Tool (motounlocktool.com, agent mapping)', 'https://motounlocktool.com/seller', 'seller page', 'Exa HTTP 500. UNKNOWN.', EXA)
N('X-FRP PRO', 'X-FRP PRO (xfrppro.com)', 'https://xfrppro.com/reseller.php', 'reseller page', 'Exa SOURCE_NOT_AVAILABLE (agent D1 located vendor). UNKNOWN.', EXA)
N('MI Byass Tool', 'Mi-Bypass (mi-bypass.com)', 'https://www.mi-bypass.com/resllers/', 'reseller page', 'Exa SOURCE_NOT_AVAILABLE. UNKNOWN.', EXA)
# vendor found, no readable list
N('Pixel Service Tool', 'Pixel Service Tool', 'https://pixelservicetool.com/', 'homepage', "No reseller list. Vendor: '$1 per credit', 'DHRU Fusion reseller API' -> HalabTech ($0.79/credit) LIKELY on vendor DHRU API, but not listed anywhere. UNKNOWN.", EXA)
N('Nice Unlocker Tool', 'Nice Unlocker Tool', 'https://niceunlockertool.net/', 'homepage', 'No reseller list; vendor sells directly (Commercial Bank/Abyssinia/Telebirr accounts of Mohammed Ebrahim, Binance). UNKNOWN.', EXA)
N('MultiUnlock Service Utility Tool', 'MultiUnlock', 'https://multiunlock.com/', 'Official Partners section', "Names not rendered except PuntoDigital (agent: PuntoDigital, Katt GSM, PowerUnlock); 'Simply contact one of our authorized resellers to complete your purchase.' UNKNOWN.", EXA)
N('Gawansmirt Unlocker Pro', 'GAWANSMIRT UNLOCKER PRO', 'https://www.gawansmirtunlockerprotool.com/', 'homepage', 'No reseller list. UNKNOWN.', EXA)
N('Powerful Unlocker Pro', 'Powerful Unlocker Pro', '', 'Exa agent A search (high)', 'No official vendor site found. UNKNOWN.', AG)
N('Mobile Unlocker Tool', 'Mobile Unlocker Tool', '', 'Exa agent A search (high)', "No official vendor site found ('Mobile Unlocker' on general-unlocker.com is a distributor, not this tool). UNKNOWN.", AG)
N('GSMunlock', 'GSMunlock (vendor unidentified)', 'https://gsmunlock.net/', 'homepage', 'gsmunlock.net is a Tajik GSM-services store (+992558006068, reseller API for sites), not the tool vendor. UNKNOWN.', EXA)
N('Laelo Samsung Unlock tool', 'Laelo Tool', 'https://laelotool.com/', 'homepage', "Placeholder template site (Lorem ipsum), no resellers. Dhru stores label it 'Laelo Samsung Unlock tool by Infinity'. UNKNOWN.", EXA)
N('Mesallah Hardware Tool', 'Mesallah', 'https://mesallah.com/resellers', 'reseller page', 'Page rendered empty. UNKNOWN.', EXA)
N('Lanrui Gzlanrui Hardware Tool', 'Gzlanrui / Lanrui', 'https://www.gzlanrui.com.cn/', 'Exa agent A', 'Official site readable, no sales-channel list. UNKNOWN.', AG)
N('PhoneMicroDB', 'PhoneMicroDB (Extended Box product page per agent)', 'https://extended-box.com/en-us/product/', 'Exa agent A', 'No named reseller list. UNKNOWN.', AG)
N('W2R Solutions Schematic', 'W2R Schematics', 'https://w2rsolutions.in/user/reseller.php', 'reseller page', "'Verified Resellers' heading but no names rendered. UNKNOWN (R6 A1: /resellers 404).", EXA)
N('YCS Drawing Bitmap', 'YCS', '', 'Exa agent A', 'No official vendor page found. UNKNOWN.', AG)
N('tool.emmc-ufs', 'EMMC&UFS Tool', 'https://tool.emmc-ufs.com/en/', 'pricing page', "'Purchase only through resellers - then activate inside the tool'; no reseller names rendered. Vendor list $10/$20/$30/$50 vs HalabTech $9.99/$19.85/$28.99/$48.99. UNKNOWN.", EXA)
N('Orion Schematics', 'Orion Schematics (PT Essential Teknologi Multimedia, Jakarta)', 'https://gsmorion.com/', 'homepage FAQ', "'You can purchase a license directly from our App or via Resellers'; no names. UNKNOWN.", EXA)
N('JC programmer', 'JCID / JC', 'https://www.jcprogrammer.com/jc-college/became-a-dealer/', 'Exa agent A', 'Dealer-application page only. UNKNOWN.', AG)
N('Refoxteam schematic', 'REFOX', 'https://www.refoxteam.com/', 'Exa agent A', 'No readable reseller list. UNKNOWN.', AG)
N('QCDMA Tool', 'QCDMA-Tool (operator محمد سيف الحيمي, Yemen)', 'https://www.qcdma-tool.com/p/sellers-agents.html', "'وكلاء البيع المعتمدون' page (Exa + Firecrawl)", 'Agent names not rendered (Blogger widget). HaliUnlock (Yemen) sells QCDMA TOOL (search snippet). UNKNOWN.', FC)
N('Gsmhelptool.com Activation', 'GSM Help Tool', 'https://gsmhelptool.com/', 'homepage', 'No reseller list. UNKNOWN.', EXA)
N('Aman Remote Technician Edition', 'Aman Remote (unidentified)', '', 'Exa agents B1 and D2 (high)', 'Vendor not identified. UNKNOWN.', AG)
N('Artemis Tool', 'Artemis II (Thai-language site)', 'https://artemis2.vip/', 'homepage', 'No reseller list. UNKNOWN.', EXA)
N('Odin Activations', 'Muslim Odin', 'https://muslimodin.com/', 'homepage', 'No reseller list. UNKNOWN.', EXA)
N('FD Tool pro', 'FDToolPro2.0 (Brazil)', 'https://fdtool.com.br/', 'homepage', 'No reseller list. UNKNOWN.', EXA)
N('iDevicePro Tool', 'iDevicePro TEAM', 'https://www.idevicepro.ru/', 'homepage', 'No reseller list. UNKNOWN.', EXA)
N('GFS PRO TOOL', 'GFS PRO TOOL (gsmfileshop.com per agent)', 'https://gsmfileshop.com/', 'Exa agent B1', 'Store homepage, no vendor list. UNKNOWN.', AG)
N('Droidmod Tool', 'Droidmod (server.droidmodguru.com per agent)', 'https://server.droidmodguru.com/', 'Exa agent B1', 'Malaysian reseller store, not a vendor list. UNKNOWN.', AG)
N('KGPROTOOL', 'KG Pro Tool Next-Gen', 'https://www.kgprotoolnextgen.com/', 'homepage', 'Pricing only (3 Month $25), no reseller list. HalabTech 3 Month $17.99. UNKNOWN.', EXA)
N('HTD', 'HTD (Build Your Store Online)', '', 'Exa agent B1', 'Vendor not identified; possibly a HalabTech in-house web-store product (unverified). UNKNOWN.', AG)
N('Android Remove Lock Screen', 'MOBILedit (Compelson) / Oxygen Forensic licences', 'https://www.mobiledit.com/resellers', 'Exa agent B1', 'Generic reseller programme; no HalabTech evidence. UNKNOWN.', AG)
N('Dr.Fone', 'Wondershare Dr.Fone', '', 'Exa agent B2 (medium)', 'Not researched beyond agent (mainstream software). UNKNOWN.', AG)
N('Orbitmobile E-Sim', 'Orbitmobile eSIM', '', 'Exa agent B2 (medium)', 'Vendor not identified. UNKNOWN.', AG)
N('Nemesis Box Activation', 'Nemesis Box', '', 'Exa agents B2 and D2', 'No official GSM-tool vendor page (R6 A1 same). UNKNOWN.', AG)
N('MaAnt Maintenance Tool', 'MaAnt', '', 'Exa agents B2 and D2', 'Vendor not identified. UNKNOWN.', AG)
N('RBM (Repair Bussiness Management)', 'RBM Borneo (Indonesia)', 'https://rbm-borneo.com/', 'homepage', "Reseller programme via admin ('How To Become Reseller 1. Contact Admin'), no list. Lead: Borneo team (A1-17 lists HalabTech as Borneo seller). UNKNOWN.", EXA)
N('Sam-Token Tool', 'SAMTOKEN', 'https://sam-token.com/', 'homepage', "'Always Buy From Trusted Resellers'; 'Distributor WorldWide / Reseller WorldWide' headings without names. UNKNOWN.", EXA)
N('F-KEY TOOL', 'F-KEY TOOL NET (Indonesia)', 'https://www.f-keytool.net/', 'homepage', "'Trusted Reseller All Roles Main Distributor Distributor Reseller' (JS list not rendered); 'Api Automation'. UNKNOWN.", EXA)
N('MDM FIX PRO', 'MDM FIX PRO / MFP TOOL (vendor unidentified)', '', 'Exa agents B2/D2', 'Agent D2 mapped it to mdmfixtool.com - rejected (different product). UNKNOWN.', AG)
N('Android Root Tool [ART]', 'Android Root Tool (androidroottool.com per agent)', 'https://androidroottool.com/faq/', 'Exa agent B2', "Agent-only excerpt: buy from the official web 'Buy Now' page or a reseller tab (not re-fetched). UNKNOWN.", AG)
N('GPixel Pro Tool', 'GPixel Pro', 'https://gpixel.pro/', 'homepage', 'No reseller list; direct credit sales. UNKNOWN.', EXA)
N('IMEIPlus Pixel Tool', 'IMEIPlus', 'https://imeiplus.com/', 'homepage', "Vendor wholesale programme ('request reseller pricing ... buy wholesale credits'); no list. Direct reseller account LIKELY but unproven. UNKNOWN.", EXA)
N('GSM Family Tool', 'GSM Family Tool (vendor unidentified)', '', 'Exa agents B2/D1', 'Agent D1 mapped it to gsmfuture.in (GFT) - rejected as a different product. UNKNOWN.', AG)
N('LIKA TOOL', 'LIKA TOOL', 'https://www.likatool.com/', 'Exa agent B2', 'Title only. UNKNOWN.', AG)
N('ONE CLICK PhoneRepair', 'One Click Tool (Sanaa, Yemen)', 'https://oneclick-tool.com/', 'homepage', 'No reseller list; prices 3m $15, 6m $20, 1y $30 (HalabTech 1y $24.99). Same street as General Unlocker. UNKNOWN.', EXA)
N('Covva Pro Tool', 'Covva Pro Tool', '', 'Exa agents B2/D2', 'Not found. UNKNOWN.', AG)
N('PhoeProgramFix Tool', 'PhoeProgramFix Tool', '', 'Exa agents B2/D2', 'Not found. UNKNOWN.', AG)
N('KRDT Utility Pro Activation', 'KRDT Utility Pro', 'https://krdtpro.com/partners', 'Exa agents B2/D1', "Partners page shows only an interstitial ('Click here to enter'). UNKNOWN.", AG)
N('A.N TOOL', 'A.N.TOOL (developer Ali Najeeb, per agent)', 'https://www.antool.io/', 'Exa agent D1', 'Direct subscription, no distributors named (agent-only). UNKNOWN.', AG)
N('S-Tool Pro', 'S-Tool Pro', 'https://app.s-tool.pro/verify', 'Exa agents B2/D1', 'Build-verification page only; no list. UNKNOWN.', AG)
N('S-Tool Pro (Windows Tool)', 'S-Tool Pro', 'https://app.s-tool.pro/verify', 'Exa agents C1/D1', 'No list. UNKNOWN.', AG)
N('MUDigital Too', 'MUDigital', '', 'Exa agents B2/D1', 'Not found. UNKNOWN.', AG)
N('053LLM TOOL', '053LLM Tool', '', 'Exa agents B2/D1', 'Not found. UNKNOWN.', AG)
N('DML TOOL PRO', 'DMLTOOL PRO', '', 'Exa agents B2/D1', 'Not found. UNKNOWN.', AG)
N('ArabFRP Tool', 'Arab FRP Support', 'https://arabfrp.com/Profile/ArabFRPTool/', 'profile page', "Only title rendered; agent saw an 'Authorized Distributors' heading without names. UNKNOWN.", EXA)
N('Taj AuthTool', 'Taj Tool (tajtool.com)', 'https://tajtool.com/', 'Exa agent D1', 'Associated domain shows unrelated/expired content. UNKNOWN.', AG)
N('SRS AUTH TOOL', 'SrsAuth Tool', '', 'Exa agent D1', 'Associated domain expired. UNKNOWN.', AG)
N('XM Auth Tool', 'XM AUTH TOOL', '', 'Exa agents C1/D1', 'No official source verified. UNKNOWN.', AG)
N('TIGER AUTH TOOL', 'TIGER AUTH TOOL', '', 'Exa agents C1/D1', 'Not found. UNKNOWN.', AG)
N('SRK FRP Tool', 'SRK FRP Tool', '', 'Exa agents C1/D1', 'Only a multi-service store found (excluded). UNKNOWN.', AG)
N('FIRE FRP Tool', 'Fire FRP Tool', 'https://firefrptool.com/', 'homepage', "'Find a Fire FRP Tool Reseller' section without names. UNKNOWN.", EXA)
N('MRPROFIXER Auth tool', 'MRPROFIXER AUTH TOOL', 'https://mrprofixer12.com/', 'homepage', 'Reseller inquiries via Telegram only; no list. UNKNOWN.', EXA)
N('OH AUTH TOOL', 'OH AUTH TOOL', 'https://ohauthtool.com/', 'homepage', "'Recharge via Distributors'; 'Purchase OH AUTH TOOL credits from our verified Dhru Fusion partners ... Loading distributors...' (dynamic list). Vendor sells only via Dhru partners; HalabTech presence UNKNOWN.", EXA)
N('Xiaomi Beast', 'Xiaomi Beast (Pakistan, +923226627110)', 'https://xiaomibeast.com/', 'homepage', 'No list. UNKNOWN.', EXA)
N('EMB AUTH TOOL', 'EMB AUTH TOOL', 'https://embauthtool.com/', 'homepage', 'No list. UNKNOWN.', EXA)
N('Anytool Auth', 'Anytool Auth', '', 'Exa agents C1/D1', 'Not found. UNKNOWN.', AG)
N('SKY AUTH TOOL', 'SKY AUTH TOOL', '', 'Exa agents C1/D1', 'Not found. UNKNOWN.', AG)
N('MiAssistant Pro Tool', 'Mi Assistant Pro', 'https://miassistantpro.com/', 'Exa agent C1', 'Premium panel for users/resellers (agent-only); no list. UNKNOWN.', AG)
N('Adam Tool', 'Adam Tool', '', 'Exa agents C1/D1', 'Not found. UNKNOWN.', AG)
N('HyperAuthTool', 'HyperAuthTool', 'https://hyperauthtool.com/', 'Exa agents C1/D1', "'reseller portal access' via Telegram/email (agent-only); names unreadable. UNKNOWN.", AG)
N('HaaFedK Xiaomi Auth', 'HaaFedK Xiaomi Auth Tool', 'https://haafedk.com/haafedkpro/XiaomiAuthTool/index.php', 'Exa agent C1', "'واجهة API للموزعين' (API for distributors) - agent-only; no list. UNKNOWN.", AG)
N('FCK Tool Xiaomi', 'FCK Tool', 'https://fcktool.com/', 'Exa agents C1/D1', 'Partner names unreadable. UNKNOWN.', AG)
N('Soul Auth Tool', 'SoulAuth', 'https://www.soulauth.com/', 'homepage', "'Authorized Resellers Purchase credits from verified distributors in your region' - names not rendered. Lead: Soul Unlocker (Kraken Big Distributor). UNKNOWN.", EXA)
N('NC AuthTool', 'NC AuthTool', 'https://ncauthtool.com/', 'Exa agent D2', 'No list. UNKNOWN.', AG)
N('Best Auth Tool', 'BestAuthTool', 'https://bestauthtool.com/', 'Exa agent D2', 'No list. UNKNOWN.', AG)
N('UK-Tools OTP', 'UK-Tools OTP', '', 'Exa agents C2/D2', 'Not found. UNKNOWN.', AG)
N('Zen Auth Tool', 'Zen Auth Tool', 'https://zenauthtool.com/', 'Exa agent D2', 'No list. UNKNOWN.', AG)
N('Nova Auth Tool', 'Nova Auth Tool', 'https://novaauthtool.com/', 'Exa agent C2', "'Our Resellers and Distributors' heading without names (agent-only). UNKNOWN.", AG)
N('Venom Auth Tool Credit', 'Venom Auth Tool', 'https://www.venomauthtool.com/', 'homepage', "Reseller list empty; vendor Dhru-compatible credit-transfer API (see family finding). UNKNOWN listing.", EXA)
N('Ultra auth Tool', 'Ultra Auth Tool', 'https://ultraauth.org/', 'homepage', 'Reseller list empty; identical Dhru-API template to Venom. UNKNOWN listing.', EXA)
N('BEST FRP TOOL', 'BEST FRP TOOL', '', 'Exa agents C2/D2', 'Not found. UNKNOWN.', AG)
N('PENGUINE MULTI TOOL', 'Penguine Multi Tool', 'https://penguintool.com/', 'Authorized Resellers', "Only 'Activeunlocker Main Distributor' named; other cards unnamed. UNKNOWN.", EXA)
N('JAT AUTH TOOL', 'JAT AUTH TOOL', '', 'Exa agents C2/D2', 'Not found. UNKNOWN.', AG)
N('Relax Auth Tool', 'Relax Auth Tool', '', 'Exa agents C2/D2', 'Not found. UNKNOWN.', AG)
N('BULK AUTH TOOL', 'BULK AUTH TOOL', 'https://www.bulkauthtool.com/api-register/', 'Exa agent D2', "'JOIN API PANEL' (agent-only) - vendor API panel; no list. UNKNOWN.", AG)
N('FRPTooLPRO', 'FRP Tool Pro', '', 'Exa agents C2/D2', 'Not found. UNKNOWN.', AG)
N('Mummy Auth Tool', 'Mummy Auth Tool', '', 'Exa agents C2/D2', 'Not found. UNKNOWN.', AG)
N('CLICK FRP TOOL (CFT)', 'Click FRP Tool', 'https://clickfrptool.com/', 'Exa agent D2', 'No list. UNKNOWN.', AG)
N('Power Tool Auth', 'Power Auth Tool', 'https://powertoolauth.com/', 'Exa agent D2', "'reseller plans available', no list (agent-only). UNKNOWN.", AG)
N('Samsung Frp', 'service SKU (FRP + Samsung account removal, Middle East)', '', 'Exa agents C2/D2', 'Not a tool vendor. UNKNOWN.', AG)
N('Xiaomi Authorized Account', "service SKU ('Custom Xiaomi')", '', 'Exa agents C2/D2', 'Not a tool vendor. UNKNOWN.', AG)
N('Meow Realme', 'Meow Realme Login Tool', '', 'Exa agents C2/D2', 'Not found. UNKNOWN.', AG)
N('Xyno Miflash', 'Xyno', '', 'Exa agents C2/D2', 'Not found. UNKNOWN.', AG)
N('FAST FRP TOOL', 'Fast Frp Tool', 'https://fastfrptool.com/', 'Distributors & Resellers section', 'Partially rendered cards (GSMNXT, GSM Vietnam, MD UNLOCKER, Gsm Egypt, IMEISTAR, GSM INDIA, GSM BRAZIL ...); HalabTech not visible but list incomplete. UNKNOWN.', EXA)
N('Gsm Auth Tool', 'GsmAuth.com (Sohaib Akram)', 'https://www.gsmauth.com/', 'homepage', 'No reseller list; GsmDone.com named as Dhru Web API partner (see finding). HalabTech not listed.', EXA)
N('P@NDONYMUS Tool', 'P@NDONYMUS', 'https://www.pandonymus.com/terms', 'Exa agent B2 (terms page)', "Agent-only excerpt: 'Each P@NDONYMUS license and account is personal, non-transferable and not for resale.' Not re-fetched; if accurate HalabTech resale is outside vendor terms. UNKNOWN.", AG)

# ---------------------------------------------------------------- group status table
groups = [l.rstrip('\n').split('\t') for l in open(TSV, encoding='utf-8')]
gid = {g[1]: g[0] for g in groups}
status = {}
for i, f in enumerate(findings, 1):
    f['tid'] = 'W5-%02d' % i
for i, d in enumerate(L):
    for g in d['groups']:
        status.setdefault(g, ('LISTED', d['conf'], d['url'], findings[i]['tid']))
octo_f = [f for f in findings if f['entity'] == 'Octoplus Box team'][0]
for g in OCTO:
    status.setdefault(g, ('LISTED (R6 A1-10)', octo_f['confidence'], octo_f['source_url'], octo_f['tid']))
for n in NEG:
    g = n['entity'].split('[HalabTech group: ')[1][:-1]
    if g not in status:
        r = n['result']
        if r.startswith('UNREACHABLE') or any(k in r for k in ('suspended', 'Parked', 'SOURCE_NOT_AVAILABLE', 'HTTP 5', 'unrelated Chinese')):
            st = 'UNREACHABLE'
        elif 'ABSENT' in r:
            st = 'ABSENT'
        elif any(k in r for k in ('Not found', 'not identified', 'No official vendor', 'No official source', 'Not a tool vendor', 'Not researched', 'unidentified', 'not the tool vendor', 'domain expired', 'unrelated/expired', 'Only a multi-service store')):
            st = 'VENDOR_NOT_FOUND'
        else:
            st = 'NO_PUBLIC_LIST_OR_NOT_RENDERED'
        status[g] = (st, '', n['url'], '')
missing = [g[1] for g in groups if g[1] not in status]
extra = [g for g in status if g not in gid]
group_status = [dict(group_id=gid[g[1]], group=g[1], halabtech_on_vendor_list=status[g[1]][0], confidence=status[g[1]][1], vendor_url=status[g[1]][2], finding=status[g[1]][3]) for g in groups if g[1] in status]

out = dict(
  stream='W5-longtail',
  tool_log=tool_log,
  findings=findings,
  negative_findings=NEG,
  new_leads=[
    'All Unlocker (allunlocker.com, +962789940944): shown with info@halabtech.com on global-unlocker-pro.com and as a Main Distributor on general-unlocker.com -> test whether it is a HalabTech-run brand acting as HalabTech\'s Yemeni-tool distributor.',
    'ADY Unlocker WhatsApp +12816728384 receives Fast Unlocker Pro direct-sale payments; ADY is the sole Tira distributor and the only worldwide reseller of TheMagicTool/GuerraTool -> compare ADY Dhru catalogue strings/prices with HalabTech Tira, Fast Unlocker Pro, Magic Tool, GuerraTool SKUs.',
    'GsmDone.com is the declared Dhru Web API partner of GsmAuth.com -> check GsmDone catalogue for the GsmAuth refill service and price.',
    'GsmEasy is the only SETool distributor named on files.setool.net -> match HalabTech LG Tool/LGE credit SKUs ($53.65, $29.45, $30.50) to GsmEasy/imei.us prices.',
    'AppleUnlockers (Gsm Anik, +8801757574757) is CF Tools Main Distributor and also a DTpro distributor -> compare its CF-Tools SKUs with HalabTech CF-Tools computed prices ($4.592/$9.53/$15.499/$21.99).',
    'Smartbe Unlock (smartbeunlock.com) is Mysterio FRP primary wholesale distributor with direct API -> check for the HalabTech-style string \'Mysterio FRP Unlock Refill (Old User) [AUTO API]\'.',
    'Cerberus seller dashboard uses role-based prices -> if any Cerberus distributor publishes Special Distributor prices, test HalabTech $24.99/$39.99/$59.99 as markup over them; keep monitoring Cerberus SKU renames vs vendor changes.',
    'Soul Unlocker (soulunlocker.com, +447519755549): Big Distributor of KrakenAuth and Worldwide Distributor of MULTIPROTOOL; possibly behind SoulAuth -> source candidate for HalabTech Kraken AUTH and Soul Auth Tool SKUs.',
    '3gsm.ru: sole distributor of Xiaomi Flasher Pro (HalabTech absent) -> candidate source for XFP SKU.',
    'GSMNXT (Telegram @XFTADMIN, +91-9547881259): distributor on Falcon FRP, Fast FRP Tool and MR AUTH -> probable XiaomiFireTool admin; map the Indian Xiaomi-auth back office.',
    'HaliUnlock (haliunlock.com, +967777600067/+967777213605) sells QCDMA TOOL and CDMA_YEMEN_TOOL -> candidate supplier for R6 D-16 (Yemen Server Box / CDMA Yemen Tool Pro).',
    "'Laelo Samsung Unlock tool by Infinity' (store label) -> check infinity-box.com online services for Laelo credits (HalabTech is an Infinity distributor, A1-05).",
    'RBM (rbm-borneo.com) appears to be a Borneo-team product -> HalabTech is a Borneo seller (A1-17); check Borneo seller panel for RBM codes.',
    'Wayback CDX for mtkgogo.com, simtool.net and kingunlock.net reseller pages (sites now down/lapsed) to test the Thai-family and King Tools distributor lists.',
    'P@NDONYMUS terms (agent-only) forbid resale -> verify the clause and whether HalabTech activations are grey-market.',
    'vpunlocker.com/pages/officialdistributor lists HalabTech as Distributor Worldwide (search snippet) - vendor/tool not in this group list; identify.'],
  open_questions=[
    'For top-tier listings (Cerberus Special Distributor, Pixel Pro Master, Eagle FRP Master, TMT Big Distributor, NEXTG sole distributor, HXRU Main Distributor, UST/MobileProTool sole partner), does HalabTech fulfil via the vendor API/panel or by manual code purchase? Needs SKU-name/ID sync evidence like the Cerberus rename.',
    'Is the unnamed iPro Auth Tool card with Telegram @HTSupport HalabTech (WhatsApp shown belongs to AsUnlocker)?',
    "Which products are HalabTech 'MDM FIX PRO' (MFP TOOL), 'GSM Family Tool', 'Aman Remote Technician Edition', 'HTD' and 'GSMunlock'? Vendors unidentified.",
    'For reseller-tier listings (Tira, Sim-Unlocker Pro, CF Tools, E-GSM, RADEX, BMT Pro), does HalabTech buy from the named distributor (ADY, HaliUnlock, AppleUnlockers, AHMET USTA/GsmSalman, Dost Service) or directly?',
    'Who supplies HalabTech for vendors that omit it (Mysterio, TheMagicTool, GuerraTool, Roby Tech, Tuna, FRP Unlock Tool, MIFRPTOOL, Xiaomi Paid, TONI, MIUI Tool, Lazy Loader, Kraken, Easy Auth, XFP, iMFC, ZXW, FCL, SETool)?',
    'Thai-family hypothesis (RTC/MTK GoGo/SimTool/GSMunlock) is untested because the MTK GoGo and SimTool sites are down or lapsed.'],
  tool_families=[
    dict(family='Yemeni Samsung/LG unlock tools', members=['General Unlocker Pro', 'Tira Unlocker', 'Fast Unlocker Pro', 'UFT-Tool', 'Sim-Unlocker Pro (via HaliUnlock)', 'Alseery Unlocker', 'QCDMA Tool', 'OneClick Tool', 'R6: Global Unlocker Pro, Hunter, Q-Unlocker, KEY-Tool'], shared_distributor='Hali Unlock, Speed Unlocker, All Unlocker, ADY Unlocker, GSM-T-TOOL', halabtech_appears='yes on every reachable list (distributor on General/Fast; reseller on Tira/Sim-Unlocker; agent on UFT)', confidence='LIKELY'),
    dict(family='Indian OTP/auth (RFT Loader = GSM Future Tool template)', members=['RFT Loader', 'GSM Future Tool', 'Nexa Pro', 'Galaxy Auth', 'Smart FRP Tool', 'Lazy Loader'], shared_distributor='Softsoln, Gsmninja, Adyunlocker (+HalabTech) top tier; GsmNinja, Gsm Fast Pro, GSM Ultimate pool', halabtech_appears='yes except Lazy Loader', confidence='LIKELY'),
    dict(family='Tanzanian/East-African MDM tools (360 TOOL = HSPRO template)', members=['360 TOOL', 'HSPRO TOOL', 'Apizu', 'Knox Wizard', 'SmartTool Pro', 'Roby Tech Tool'], shared_distributor='FRP King Server, UnlockerBD, Ohideraunlocker, GMS RESELLER, East-African resellers', halabtech_appears='yes except Roby Tech Tool', confidence='LIKELY'),
    dict(family='FalconMultiTool Team', members=['OPlusPro (OPlusProLogin)', 'Falcon Multi Tool'], shared_distributor='GSM Manager (Main Distributor)', halabtech_appears='yes (Distributor WorldWide on both)', confidence='CONFIRMED (same Owner shown on both vendor pages)'),
    dict(family='Bangladeshi FRP-King/Clean-Unlocker template', members=['Falcon FRP Tool', 'Xiaomi Service Tool'], shared_distributor='FRPKING, CLEANUNLOCKER', halabtech_appears='yes', confidence='UNKNOWN (template only)'),
    dict(family='Dhru-API white-label auth', members=['Venom Auth Tool', 'Ultra Auth Tool'], shared_distributor='vendor Dhru credit-transfer API', halabtech_appears='lists empty', confidence='LIKELY (identical sites)'),
    dict(family='Reseller-panel template', members=['Eagle Multi Tool', 'Xiaomi Paid Tool'], shared_distributor='none', halabtech_appears='Eagle yes; Xiaomi Paid no', confidence='UNKNOWN'),
    dict(family='Brazil-linked FRP template', members=['Tuna Pro Tool', 'FRP Unlock Tool', 'Penguine Multi Tool', 'MIFRPTOOL.COM'], shared_distributor='supremegsm/FRP BRASIL; Activeunlocker', halabtech_appears='no (absent on readable lists)', confidence='UNKNOWN'),
    dict(family='Motorola template', members=['TheMagicTool', 'GuerraTool'], shared_distributor='ADY UNLOCKER, MENDOZA GSM, GUERRADONE', halabtech_appears='no', confidence='UNKNOWN'),
    dict(family='BMT Pro = iPro Auth Tool template', members=['BMT Pro', 'iPro Auth Tool'], shared_distributor='identical reseller roster', halabtech_appears='yes on BMT (Reseller); likely on iPro', confidence='LIKELY'),
    dict(family='Turkish partner network', members=['CheckerTR PRO', 'RADEX FRP', 'MIUI Tool', 'CP Tool', 'E-GSM', 'Xiaomi Anonymouse', 'NEXTG'], shared_distributor='Dost Service, IMEI ve SERVER, Unlock Bayi, OFFUNLOCK, VIP Pro Support', halabtech_appears='yes except MIUI Tool', confidence='UNKNOWN'),
    dict(family='Thai tools (hypothesis)', members=['RTC Tool', 'Artemis II', 'MTK GoGo', 'SimTool', 'GSMunlock'], shared_distributor='not established', halabtech_appears='RTC yes (R6 A2-17); others unknown', confidence='UNKNOWN')],
  group_status=group_status,
  coverage=dict(groups_in_input=len(groups), groups_recorded=len(status), missing=missing, unknown_group_names=extra,
                exa_agent_runs=7, exa_agent_cost_usd=2.30, verified_positive_vendor_pages=sum(1 for f in findings if 'R7 verification: page fetched' in f['notes']),
                verified_negative_pages=sum(1 for n in NEG if n['tool'] != AG and ('ABSENT' in n['result'] or 'not listed' in n['result'] or 'No list' in n['result'])))
)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', OUT, 'findings', len(findings), 'neg', len(NEG), 'groups', len(status), 'missing', missing, 'extra', extra)
