# NEXT RESEARCH MISSION: HalabTech Round 8 (prepared 2026-10-11)

## State after Round 7

Unit: the 10:03 UTC catalog (383 groups, 1,455 SKUs).

| Measure | Value |
|---|---|
| Coverage (groups checked at least once) | 342 / 383 = 89.3% |
| Attribution (SKUs with upstream ≥LIKELY) | 601 / 1,455 = 41.3% |
| Verification (CONFIRMED immediate source) | 21 / 1,455 = 1.4% (in-house only) |
| UNKNOWN | 189 groups / 849 SKUs |
| DISPUTED | 1 group / 5 SKUs |
| Developers that officially list HalabTech | 125 (CONFIRMED or STRONG) |
| Named third-party API suppliers proven for a specific service | 0 |

**STRONG chains:**
- Sigma → GsmServer (exclusive distributor; panel credits bought on GsmServer) → HalabTech.
- Chimera → {GsmEasy | GsmServer | Unlock.eu} → HalabTech.
- Hunter Unlocker, Q-Unlocker and XTP → HalabTech (direct).
- GsmServer Products (2020–2024).

**LIKELY chains:**

| Candidate | HalabTech services |
|---|---|
| Fast Unlocking | UMT, NCK, Avengers |
| GSM Nigeria | Alseery, F-KEY |
| Cerberus (vendor API) | Cerberus |
| GSMFATHER | Moldova |
| GsmDone | GsmAuth |
| GsmEasy | SETool |
| AppleUnlockers | CF Tools |
| ADY Unlocker | Tira, TheMagicTool, GuerraTool, Panda |
| GsmUnlockingStore | Samsung FRP Source #3, April 2026 batch |

**DISPUTED:** Code-GSM → HalabTech for T-Mobile Clean & Paid Off (REL-097).

**Reversed (now downstream customers):** UnlocksPro; Code-GSM for the Mi Account family.

## Questions, methods and completion criteria

| # | Question (case) | Public, lawful method | Done when |
|---|---|---|---|
| 1 | Who sells the T-Mobile Premium unlocks at exactly $115.00 / $125.00? (GAP-023) | Hourly snapshots of T-Mobile premium sellers. Detect HalabTech re-pricing events (the markup moved from x1.06 to x1.045 on 11 Oct). | A seller at $115/$125, or one whose price moves in step with HalabTech. |
| 2 | Which server owns native IDs 3277–3281 (T-Mobile Clean & Paid Off)? Did Code-GSM list these tiers before 2 Mar 2026? (GAP-014) | Web search for the ID-prefixed names. Wayback and Telegram first-appearance dates per tier. | Origin server named, or Code-GSM's first date fixed. |
| 3 | Is GSM Nigeria upstream for Alseery/F-KEY/CPID, or a HalabTech dealer? (GAP-024) | Paired daily price series. Wayback first appearance of "Hydra Digital Actiavtion" and of the "Netowrk ... CPID - Direct Distributor" group. | Direction shown by dates or synchronous moves. |
| 4 | Identities of the numbered IMEI sources (Samsung FRP #1–#4, MDM #2/#3, Mi Account routes) (GAP-027) | Correlate HalabTech's automatic Telegram "Service Active/Inactive" posts with candidates' public status posts. Look for ID or label artefacts. | At least 1 source named, or narrowed to 2 or fewer candidates. |
| 5 | Samsung CPID / EDL / JDM operators (61 SKUs) (GAP-028) | Same-day price capture of nevutek, imeishop, serverunlocker and GSM Nigeria detail pages. | Price or ID match for at least 1 group. |
| 6 | iRemove FMI OFF iPad/iWatch channel (60 SKUs) (GAP-016) | Model-by-model offsets against at least 5 sellers at one timestamp. | A constant offset to one seller, or all excluded. |
| 7 | HalabTech dealer tiers (Reseller / Big Reseller / Web Owner) (GAP-031) | Archived DISTRIBUTOR page; Telegram tier posts. | Tier table recovered; all price tests recalibrated. |
| 8 | Top-tier vendor fulfilment: API or manual? (GAP-029) | Twice-daily catalog snapshots to catch name or price syncs like the Cerberus rename. | At least 3 vendors show a sync event, or none in 14 days. |
| 9 | GSX IDs #225/#33225/32596 and the Signal Labs supplier (GAP-025, GAP-026) | 2020 Wayback captures of GSX-check servers. Priced Signal Labs listings at the implied costs. | Origin named, or ruled out. |
| 10 | Which Chimera distributor? (GAP-011) | Synchronous price-change test across GsmEasy, GsmServer, Unlock.eu and HalabTech. | One distributor matched. |

## Rules to keep
- An official listing proves an authorised channel, not the route orders are fulfilled through.
- Identical names or similar prices are leads only. Most matches are HalabTech's own customers.
- HalabTech's dealers undercut its public list, so "cheaper" does not mean "upstream".
- "Miniutes" is a Dhru platform default, not a fingerprint.
- GSM-Forum dates are MM-DD-YYYY.
- Use public sources only: no logins, no private endpoints, no chatbot prompting, no rate-limit evasion.
- Append only: R8 rows start at EV-492, NEG-199, CL-049 and GAP-034.
