# HalabTech supply-chain intelligence: Round 7 investigation summary

**Verification date:** 2026-10-11

**Unit of analysis:** the public catalog of server.halabtech.com, captured with Firecrawl at 10:03 UTC. It has 383 groups and 1,455 SKUs. The IMEI list was re-captured at 10:39 UTC and was unchanged.

**Workbook:** `HalabTech_Complete_Supply_Chain_Research.xlsx`, 28 sheets.
- 11 new R7 sheets come first.
- The 17 sheets from Rounds 1–6 follow, unchanged (checked cell by cell).

**Confidence scale:** CONFIRMED / STRONG / LIKELY / UNKNOWN / DISPUTED. "Probable" (LIKELY or STRONG) is never counted as CONFIRMED. Every percentage below states its numerator and denominator.

## How Round 7 was run

**Research streams.** Seven streams ran in parallel, followed by a verification stream:

| Stream | Scope |
|---|---|
| W1 | Website, DNS, CT, Wayback and public JavaScript |
| W2 | Numbered IMEI sources |
| W3 | Code-GSM and UnlocksPro |
| W4 | Tool chains (Chimera, Sigma, EFT, UMT, Furious Gold, …) |
| W5 | The 205 never-checked groups |
| W6 | Catalog genealogy across 28 servers |
| W7 | Digital goods |
| V7 | Lead verification and Phase-5 second-tool re-checks |

**Tool calls.** 312 MCP calls were made, and 32 of them failed:
- Firecrawl: 132 (scrape 94, search 36, developer search 2)
- Parallel: 97 (search 41, fetch 56)
- Exa: 83 (fetch 58, agent 15, search 10)

**Output.**
- 225 findings, registered as EV-267 … EV-491.
- 198 negative checks, registered as NEG-001 … NEG-198.

**Access limits.** Only public pages and publicly served files were read. There were no logins, no probing of private endpoints and no chatbot prompting. The sandbox's own network is blocked for the target hosts; all fetching went through the MCP tools, and the block was not worked around.

**Unavailable sources.**
- crt.sh returned 502 (CertSpotter was used instead).
- saudi-gsm.com returned a Cloudflare error.
- gsmfather.com's price page now returns 404.
- Exa could not render two HalabTech Telegram posts.

**Phase-5 corrections (all logged; the raw stream files are kept unmodified):**
- **"Miniutes" withdrawn as a HalabTech marker.** It is a Dhru platform default and appears on unrelated servers.
- **Date misread in W3-03.** GSM-Forum prints dates as MM-DD-YYYY, so "04-02-2026" is 2 April, not 4 February.
- **Hydra not upgraded to STRONG.** The live vendor shop no longer shows the $1.00/credit retail price the upgrade depended on.
- **GsmUnlockingStore MDM price ratio downgraded.** It rested on two manual "charm" prices.
- **HalabTech dealer discount re-measured.** Dealers sell 2.8–12.5% below HalabTech's public list, not 8–12%.

**Second-tool checks.** 12 of the 18 STRONG/CONFIRMED findings from W2–W4, W6 and W7 were re-checked with a different tool. The other six are single-tool:
- HalabTech's own Telegram and news statements
- GSM Tiger
- Saudi-GSM (site unreachable)
- the Dhru-resale snippet

## 1. Who are the strongest candidates supplying HalabTech?

| Rank | Candidate | Supplies (HalabTech groups / SKUs) | Confidence | Basis | Main caveat |
|---|---|---|---|---|---|
| 1 | **GsmServer** | Sigma Plus licences and activations (2 groups / 5 SKUs). Historically the "GsmServer Products" group (2020–2024). | STRONG | Sigma names GsmServer its exclusive distributor, and resellers must buy panel credits on GsmServer's website (EV-491). HalabTech's costs fall inside GsmServer's panel-credit tiers (EV-319). HalabTech's own 2020–2024 catalog labelled a group "GsmServer Products" (EV-273, EV-476). | HalabTech sells 6–13% below Sigma's RRP, although Sigma allows at most a 5% discount. |
| 2 | **GsmEasy, GsmServer or Unlock.eu** | Chimera (5 SKUs) | STRONG that HalabTech buys from a distributor; UNKNOWN which one | Chimera resellers may only buy credits from distributors. HalabTech's implied cost of $0.092/credit equals all three distributors' reseller price (EV-316, EV-317, EV-477). | The three are not separable by price. |
| 3 | **Hunter Unlocker, Q-Unlocker, XTP** (developers, direct) | 5 SKUs | STRONG | Each vendor sells only through 3 listed distributors and HalabTech is one of them (EV-468, EV-469); XTP calls HalabTech its "Official Main Seller". | No API trace. |
| 4 | **Fast Unlocking** (the NCK & UMT team's activation server) | UMT, NCK and Avengers (5 groups / 13 SKUs) | LIKELY | The only distributor priced at or just below HalabTech; offers API support to other servers (EV-322, EV-479). | Non-public API prices. |
| 5 | **GSM Nigeria** | Alseery and F-KEY (4 SKUs) | LIKELY | Its prices are exactly HalabTech's implied costs ($0.68 and $1.08), checked with two tools (EV-439, EV-483). | The relationship is two-way: it also resells HalabTech credits and copies a HalabTech group typo. |
| 6 | **Cerberus** (vendor seller API) | 3 SKUs | LIKELY | Lists HalabTech first as "Special Distributor" (two tools). Offers sellers a DHRU-compatible API. HalabTech's SKUs were renamed to the vendor's product names between 02:00 and 10:03 UTC (EV-406, EV-409, EV-466, EV-481). | HalabTech's prices are not one markup over the vendor's public prices. |
| 7 | **GSMFATHER** or its upstream | Moldova (2 SKUs) | LIKELY | GSMFATHER's own service IDs 1351#/1352# are embedded in HalabTech's SKU names (EV-441, EV-485). | The page now returns 404, so the evidence is single-tool. |
| 8 | **GsmDone** (GsmAuth); **GsmEasy** (SETool); **AppleUnlockers** (CF Tools); **ADY Unlocker** (Tira, TheMagicTool, GuerraTool, Panda) | 1–8 SKUs each | LIKELY | Each developer's own page names the channel: Dhru API partner, sole distributor, Main Distributor or only worldwide reseller. | HalabTech may hold an unlisted direct account. |
| 9 | **GsmUnlockingStore** | Samsung FRP "Source #3" batch of April 2026 (now retired) | LIKELY | Identical names posted the same day as HalabTech's "Source #3" post. | HalabTech posted about 5 hours earlier; the relationship is two-way. |

**Rejected or reframed as suppliers:**
- **UnlocksPro** is a HalabTech customer, not a supplier. It resells HalabTech-proprietary products in contiguous import blocks. The R6 upstream hypothesis (REL-098) is now DISPUTED; the reverse direction is STRONG.
- **Code-GSM** is a HalabTech customer for the Mi Account family: it carries HalabTech's internal label "Source2 #Cheaper". It also resells HalabTech memberships. For "T-Mobile Clean & Paid Off" the verdict is **DISPUTED**: HalabTech's post on 2 March 2026 is the earliest dated appearance, and a third server sells the same names under IDs 3277#–3281#.

## 2. Which relationships are verified?

**CONFIRMED** means a primary source documents the link.

**Authorisation (the developer names HalabTech):**
- 125 developers document HalabTech as distributor, reseller or agent at CONFIRMED or STRONG level: 62 known in R6, 62 newly confirmed in R7, and Zhizhen at STRONG.
- These cover 455 SKUs in 149 groups.
- An official listing proves an authorised channel. It does **not** prove that HalabTech's orders are fulfilled through that account.

**Distribution structure above HalabTech (vendor documents):**
- Sigma → GsmServer: exclusive distributor, and resellers buy panel credits on GsmServer's site.
- Chimera → distributors only.
- UMT → Fast Unlocking.
- SETool → GsmEasy.
- CF Tools → AppleUnlockers (Main Distributor).
- Tira → ADY Unlocker (sole distributor).
- GsmAuth → GsmDone (Dhru Web API).

**In-house:**
- 6 groups / 21 SKUs: memberships, HalabTech Point, file requests, bundles and test SKUs.

**Downstream (HalabTech → customer), documented on the customers' own pages:**
- GsmServer, HOS Unlocker, WARD, MW Unlocker, ReUnlocker, univgsm, UnlocksPro and Code-GSM.
- Most were checked with two tools.
- univgsm prices HalabTech's internal "TEST API IMEI" at exactly 1.08 × HalabTech's price.

**Platforms:**
- Dhru Fusion (server)
- JoudiSoft Real Easy Store (support site)
- HTD (store)
- Cloudflare and GoDaddy
- Layout Team (hosting)

**Not verified:**
- No third-party supplier is documented for any specific HalabTech service: **0 SKUs**.
- HalabTech's own labels confirm at least four parallel numbered IMEI sources, but none is named.

## 3. Which developers, distributors and API providers appear in the chain?

**Original developers:**
- Server SKUs: 842 of 985 (277 groups) have a developer identified by an official site, vendor-register entry or issuer brand.
- Developers that list HalabTech: 125.
- Developers that checked and omit HalabTech: Furious Gold, UMT/NCK, Avengers, UFI, SamKey, AMT, MH Unlocker and EFT (from R6), plus 18 found in R7. The R7 group includes Mysterio, TheMagicTool, GuerraTool, ZXW, FCL, MFC, SETool and Xiaomi Flasher Pro.

**Master distributors and intermediaries named:**
- GsmServer, GsmEasy, Unlock.eu, Fast Unlocking
- ADY Unlocker, AppleUnlockers, GSM-Sources, 3gsm.ru
- Dost Service, FRP BRASIL, Soul Unlocker, Smartbe Unlock
- Hali-Unlock, Easy Team, GSM Nigeria, GSMFATHER

**API providers with published reseller APIs:** these show a route exists, not that HalabTech uses it.
- Cerberus (DHRU-compatible API)
- Apizu (Reseller API for Dhru)
- Sim-Unlocker Pro (per-reseller API)
- GsmDone (Dhru Web API)
- Venom/Ultra Auth (Dhru credit API)
- Eagle FRP, TMT Pro, Mysterio
- Fast Unlocking (API support for other servers)
- HTD (DHRU / HTD Scripts APIs)

**Unnamed API suppliers, identified by fingerprint only:**
- The T-Mobile Premium source at $115.00 / $125.00.
- The GSX source whose IDs #225, #33225 and 32596 have appeared in HalabTech's names since 2020.
- The Signal Labs source, with implied costs of $17.95 / $21.95 / $4.50 / $5.53.
- The server whose IDs 3277#–3281# carry the T-Mobile Clean & Paid Off names.
- HalabTech's numbered "Source #1–#4".

## 4. How many services trace to a defensible upstream?

| Measure (SKUs, out of 1,455) | R6 | R7 |
|---|---|---|
| Upstream at ≥LIKELY, including in-house | 400 (27.5%) | **601 (41.3%)** |
| – in-house | – | 41 (21 CONFIRMED + 20 LIKELY) |
| – third-party, named entity | – | 484 |
| – third-party, only the vendor's channel known | – | 76 |
| Third-party STRONG | 15 | 15 (Sigma 5, Chimera 5, Hunter 2, Q-Unlocker 2, XTP 1) |
| Third-party CONFIRMED immediate supplier | 0 | **0** |
| DISPUTED | 0 | 5 (T-Mobile Clean & Paid Off tiers) |
| UNKNOWN | 1,055 | 849 (189 groups) |

The 484 "named entity" SKUs break down by route:

| Route | SKUs |
|---|---|
| Developer direct by official listing | 412 |
| Vendor API | 8 |
| Named intermediary | 43 |
| Named fingerprint candidate | 6 |
| Vendor rule | 15 |

The 412 developer-direct SKUs are LIKELY, not verified. They rest on the developer's listing, not on a trace of how orders are fulfilled.

## 5. What percentage of the investigation is complete?

There is no single honest number, so three are reported, each with its formula.

| Measure | Formula | R6 | R7 |
|---|---|---|---|
| **A. Coverage** | groups checked at least once ÷ 383 | 118 (30.8%) | **342 (89.3%)** |
| **B. Attribution** | SKUs with an upstream at ≥LIKELY ÷ 1,455 | 27.5% | **41.3%** |
| **C. Verification** | SKUs with a CONFIRMED immediate source ÷ 1,455 | – | **1.4%** (in-house only; third-party 0%) |

**Reading:**
- Mapping is nearly complete. 41 groups (170 SKUs) remain unexamined: 36 carrier/OEM IMEI groups and 5 web-service groups (four cron-job products and social-media services).
- Attribution is below half.
- Verification of third-party supply is not reachable from public sources unless a supplier or HalabTech discloses it.

## 6. What is new compared with Round 6?

**Long tail closed:**
- All 205 never-checked groups were recorded.
- 80 groups are now linked to a developer that lists HalabTech: 72 found in R7, plus 8 Octoplus groups mapped from R6.
- 18 groups have vendor lists that omit HalabTech; 15 of these now have a named or listed channel.
- Vendor listings rose from 62 to 125.

**Price forensics:**
- 232 SKUs have computed (3-decimal) prices; 73 groups share a single markup.
- New fingerprints: T-Mobile Premium at $115/$125, with HalabTech's markup cut from 6.0% to 4.5% at 10:03 UTC. Also Chimera at $0.092, the Sigma panel tiers, GSM Nigeria's exact matches, and Octoplus at $0.10.

**Direction reversals:**
- UnlocksPro and Code-GSM (Mi Account) are downstream customers.
- REL-097 (Code-GSM → HalabTech) moves from LIKELY to DISPUTED.
- CL-013 is resolved: R6 compared against a stale cached copy.

**New named intermediaries:**
- Fast Unlocking (UMT/NCK/AVB)
- GsmDone (GsmAuth)
- AppleUnlockers (CF Tools)
- GsmEasy (SETool)
- GSMFATHER (Moldova)
- GSM Nigeria (Alseery, F-KEY)
- ADY Unlocker (Tira, TheMagicTool, GuerraTool)

**Sigma chain strengthened:**
- Resellers must buy panel credits from GsmServer.
- "GsmServer Products" (REL-028) moves from LIKELY to STRONG, now dated from 2020.

**Cerberus:**
- HalabTech is "Special Distributor".
- The vendor offers a DHRU-compatible API.
- HalabTech's SKU names changed to the vendor's names during the day.

**Website forensics:**
- No supplier is named in any public HalabTech HTML, JavaScript, sitemap or subdomain.
- Hosting is on Layout Team's server; the store runs on HTD.
- The chat is in-house (n8n). HalabTech sells an "AI Bot For Gsm Site" product, and its chatsosogsm/chatmenet subdomains point to buyers.

**Digital goods:**
- Syriatel SKUs are the operator's official denominations; the recharge channel is unknown.
- Google Play Turkey prices are tied to the TL face value at 47.227 TRY/USD.
- Game codes come from HalabTech's own pre-bought stock.

**Calibration:**
- HalabTech dealers sell 2.8–12.5% below its public list, so "cheaper than HalabTech" does not mean "upstream".

**Confidence changes (27 entries, CL-022 … CL-048):**

| Change | Groups |
|---|---|
| UNKNOWN → LIKELY | 102 |
| LIKELY → UNKNOWN (Signal Labs, Xiaomi Checker, JDM V4 V5, USA Reseller Flex) | 4 |
| LIKELY → DISPUTED | 1 |

## 7. What specific questions should Round 8 target?

1. **T-Mobile Premium.** Which server sells the two Premium unlocks at exactly $115.00 / $125.00?
   - Method: hourly snapshots of T-Mobile premium sellers; watch for HalabTech re-pricing events.
2. **T-Mobile Clean & Paid Off.** Which server owns native IDs 3277–3281?
   - Did Code-GSM list these tiers before 2 March 2026? Check Wayback and the Code-GSM Telegram.
3. **GSM Nigeria.** Is it upstream or a HalabTech dealer?
   - Method: a paired daily price series for Alseery, F-KEY and Hydra.
   - Also date the first appearance of "Hydra Digital Actiavtion" and of the "Netowrk" CPID group on each side.
4. **Numbered IMEI sources.** Who are Source #1–#4 (Samsung FRP, MDM #2/#3, Mi Account)?
   - Method: correlate HalabTech's automatic "Service Active/Inactive" Telegram posts with candidates' public status posts.
5. **CPID / EDL / JDM (61 SKUs).** Run same-day price captures of nevutek, imeishop, serverunlocker and GSM Nigeria's "Direct Distributor" group.
6. **iRemove FMI OFF (60 SKUs).** Run a model-by-model price-offset test across at least 5 sellers at one timestamp. A constant offset to one seller would identify the source.
7. **HalabTech's dealer tiers.** Recover the Reseller / Big Reseller / Web Owner discount table. It calibrates every price test.
8. **Top-tier vendors (Cerberus, Pixel Pro, Eagle FRP, TMT, NEXTG, HXRU, UST, MobileProTool, Apizu, CheckerTR).** Take twice-daily catalog snapshots to catch API name or price syncs like the Cerberus rename.
9. **GSX IDs #225 / #33225 / 32596** and the Signal Labs supplier. Search 2020 Wayback captures of GSX-check servers, and priced Signal Labs listings at the implied costs.
10. **Chimera.** Is the distributor GsmEasy, GsmServer or Unlock.eu? Test synchronous price changes across the three distributors and HalabTech.

---

## ملخص عربي

**هذا الملخص مبني على الكتالوج العام بتاريخ 2026-10-11 الساعة 10:03 UTC: ‏383 مجموعة و1,455 خدمة.**

**النطاق والمنهج:** نُفّذت 312 عملية بحث عبر Firecrawl وParallel وExa، أُنتج منها 225 دليلًا و198 فحصًا سلبيًا. استُخدمت المصادر العامة فقط، دون أي دخول بحساب أو فحص لواجهات خاصة.

**أقوى المرشحين للتوريد:**
- **GsmServer** لمنتجات Sigma (قوي). Sigma تسميه موزعها الحصري، وتشترط شراء أرصدة لوحة البيع منه.
- أحد موزعي Chimera الثلاثة: GsmEasy أو GsmServer أو Unlock.eu (قوي أنه موزع، والهوية غير محسومة).
- الشراء المباشر من Hunter وQ-Unlocker وXTP (قوي).
- **Fast Unlocking** لخدمات UMT وNCK وAvengers (مرجّح).
- **GSM Nigeria** لأداتي Alseery وF-KEY (مرجّح؛ تطابق تام مع التكلفة الضمنية، والعلاقة باتجاهين).
- **Cerberus** عبر واجهة البيع البرمجية للمطوّر (مرجّح).
- **GSMFATHER** لخدمات Moldova (مرجّح).

**تصحيحات الاتجاه:** UnlocksPro عميل لدى HalabTech وليس موردًا. وCode-GSM عميل في عائلة Mi Account. أما مجموعة T-Mobile Clean فأصبحت «متنازعًا عليها».

**المؤكَّد:**
- 125 مطوّرًا يذكرون HalabTech رسميًا كموزّع أو بائع، وهذا يثبت قناة معتمدة لا مسار التنفيذ الفعلي.
- 21 خدمة داخلية.
- عملاء لاحقون موثّقون من صفحاتهم.
- **لا يوجد أي مورد خارجي مؤكَّد لخدمة محددة (صفر).**

**نسب الإنجاز:**
- التغطية 89.3%: ‏342 من 383 مجموعة فُحصت مرة واحدة على الأقل.
- الإسناد 41.3%: ‏601 خدمة لها مصدر بدرجة «مرجّح» فأعلى (كانت 27.5% في الجولة السادسة).
- التحقق 1.4%: داخلي فقط.

**الأولويات للجولة الثامنة:**
- مصدر T-Mobile Premium بسعر 115/125 دولارًا.
- مالك المعرّفات 3277#–3281#.
- اتجاه العلاقة مع GSM Nigeria.
- هويات المصادر المرقّمة.
- مشغّلو CPID وEDL.
- قناة iRemove.
- جدول خصومات الوكلاء لدى HalabTech.

---

**Files:**
- The workbook (11 new R7 sheets first).
- `reports/NEXT_RESEARCH_MISSION_R8.md`.
- `data/r7/`: findings W1–W7 and V7 (raw and unmodified), catalog snapshots, verification captures and the build scripts.
