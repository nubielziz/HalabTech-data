"""Category + fulfilment-model classification for HalabTech catalog groups (rule-based, transparent)."""
import re

IMEI_RULES = [
    (r'iCloud Remove|iREMOVE', 'iCloud / FMI removal'),
    (r'Check|GSX|Checker|Financial Status', 'IMEI / GSX checker'),
    (r'Repair Netowrk|Repair Network|JDM', 'Samsung network repair / CPID'),
    (r'FRP', 'FRP removal (IMEI / remote)'),
    (r'MDM|\bID\b|HeyTap|Mi Account', 'Account / MDM removal'),
    (r'REMOTELY|Remotely|Bootloader|Signal Labs', 'Remote service / remote tool'),
    (r'Network|T-MOBILE|AT&T|USA|UK O2|SoftBank|Altice|Spectrum|XFINITY|Reseller Flex|eSIM|E-SIM', 'Carrier unlock (IMEI)'),
    (r'.', 'OEM unlock code / IMEI service'),
]

SERVER_RULES = [
    (r'^(HALABTECH|HalabTech Point|Request Files|White Friday Offer)', 'HalabTech own product'),
    (r'Syriatel|MTN|PAY CELL|Turkcell|Turk Telekom', 'Telecom top-up'),
    (r'ITUNES|ITunes|Google Play|Playstation|Pubg|Free Fire', 'Gift card / game top-up'),
    (r'AI Tools|Social media|Custom Email|EC Store|Sultankoo', 'Digital accounts / subscriptions'),
    (r'Build Your Server|Web Hosting|Cron|AI Bot For Gsm|API Test', 'Platform / hosting / test'),
    (r'Sharing Box', 'Remote box sharing (in-house hardware)'),
    (r'^Box & Dongle$', 'Physical hardware'),
    (r'Schematic|ZXW|XinZhiZao|Borneo|JC programmer|Refox|Orion|DZKJ|FCL|W2R|Zhizhen|YCS|PhoneMicroDB|Lanrui|Hardware|Panda Tools|tool\.emmc', 'Schematics / hardware-repair software'),
    (r'Octoplus|Octopus|Z3X|Pandora|UMT|NCK|Infinity|CM2|DC-UNLOCKER|DC-Unlocker|HCU|Sigma|Furious|Hydra|Easy Jtag|EFT|Chimera|Avengers|UFI|Setool|Nemesis|Box|Dongle|MWorker|Griffin|Medusa', 'Box / dongle activation & credits'),
    (r'.', 'Software tool licence / credits'),
]

# Groups that are, on their face, fulfilled in-house (HalabTech's own product, own hardware or own team).
IN_HOUSE_HINT = {
    'HALABTECH': 'Own firmware-membership product',
    'HalabTech Point': 'Internal balance transfer (point.halabtech.com)',
    'Request Files (Combination & Debug)': 'HalabTech file-request desk',
    'White Friday Offer': 'HalabTech bundle of own + third-party products',
    'Sharing Box': 'Remote sharing of boxes HalabTech physically owns',
    'Box & Dongle': 'Physical hardware shipped 1-3 days (stock source unknown)',
    'Xiaomi Auth REMOTELY SERVICES': 'TeamViewer job using HalabTech auth credits (operator unknown)',
    'Custom Email': 'Service setup',
    'Web Hosting': 'Hosting resale (host provider unknown)',
    'AI Bot For Gsm Site': 'HalabTech AI assistant (same bot as on its own sites)',
    'API Test': 'Internal test services',
    'API test': 'Internal test services',
}


def categorise(catalog, group):
    rules = IMEI_RULES if catalog == 'IMEI' else SERVER_RULES
    for pat, cat in rules:
        if re.search(pat, group, re.I if catalog == 'IMEI' else 0):
            return cat
    return 'Other'


def delivery_model(group, services):
    names = ' '.join(s['service'] for s in services)
    if group in IN_HOUSE_HINT:
        return 'In-house (likely)', IN_HOUSE_HINT[group]
    if re.search(r'AUTO API|Auto API|\bAPI\b', names):
        return 'Automated API (supplier unnamed)', 'Service names carry "AUTO API" / "API"'
    if re.search(r'Source ?#?\d|Source\d|Direct Source|Server Direct', names):
        return 'Multi-source routing (sources unnamed)', 'Service names carry "Source #n" / "Direct"'
    return 'Unknown', ''
