import os
import time
import requests
from datetime import datetime
import phonenumbers
from phonenumbers import (
    geocoder, carrier, number_type, timezone,
    is_valid_number, is_possible_number,
    region_code_for_number,
    PhoneNumberFormat, format_number
)
from colorama import init, Fore

init(autoreset=True)

# ─────────────────────────────────────────────────────────────
#  PhoneXtract v3.0
#  Created by : Alok Thakur | YouTube : Firewall Breaker
#  For Educational & OSINT Use Only
# ─────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
#  SCREEN & BANNER
# ══════════════════════════════════════════════════════════════

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    print(Fore.GREEN  + "=" * 60)
    print(Fore.CYAN   + r"  ____  _                     __  __  _                   _  ")
    print(Fore.CYAN   + r" |  _ \| |__   ___  _ __   ___\ \/ / | |_ _ __ __ _  ___| |_")
    print(Fore.CYAN   + r" | |_) | '_ \ / _ \| '_ \ / _ \\  /  | __| '__/ _` |/ __| __|")
    print(Fore.CYAN   + r" |  __/| | | | (_) | | | |  __//  \  | |_| | | (_| | (__| |_")
    print(Fore.CYAN   + r" |_|   |_| |_|\___/|_| |_|\___/_/\_\  \__|_|  \__,_|\___|\__|")
    print(Fore.GREEN  + "  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(Fore.YELLOW + "  PhoneXtract v3.0          --  Number Intelligence Tool")
    print(Fore.YELLOW + "  For Educational & OSINT Use Only")
    print(Fore.MAGENTA+ "  Created by : Alok Thakur  |  YouTube : Firewall Breaker")
    print(Fore.GREEN  + "=" * 60)


def loading_bar(label="Analyzing", total=30):
    print(Fore.CYAN + f"\n  {label} ", end="", flush=True)
    for _ in range(total):
        time.sleep(0.02)
        print(Fore.GREEN + "#", end="", flush=True)
    print(Fore.GREEN + "  DONE\n")


def save_report(report_text, number):
    safe  = number.replace("+", "").replace(" ", "_")
    ts    = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"report_{safe}_{ts}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(Fore.GREEN + f"\n  [+] Report saved --> {fname}")
    return fname


# ══════════════════════════════════════════════════════════════
#  PHONE HELPERS
# ══════════════════════════════════════════════════════════════

def get_phone_type_str(t):
    return {
        0:  "Fixed Line",
        1:  "Mobile",
        2:  "Fixed Line / Mobile",
        3:  "Toll Free",
        4:  "Premium Rate",
        5:  "Shared Cost",
        6:  "VoIP",
        7:  "Personal Number",
        8:  "Pager",
        9:  "UAN",
        10: "Voicemail",
        27: "Unknown"
    }.get(t, "Unknown")


def get_sim_type(t):
    if t == 1:  return "Likely Prepaid   (Mobile)"
    if t == 0:  return "Likely Postpaid  (Fixed Line)"
    if t == 6:  return "VoIP / Internet"
    return "Cannot Determine"


def get_call_type(parsed):
    return "Domestic  (Local / STD)" if parsed.country_code == 91 else "International  (ISD)"


# ══════════════════════════════════════════════════════════════
#  REGION / STATE DETECTION
# ══════════════════════════════════════════════════════════════

def get_region(parsed, national_num):
    """
    India   --> prefix-based state map (accurate)
    Others  --> phonenumbers geocoder (city/region where available)
    """
    if parsed.country_code == 91:
        return get_india_state(national_num)
    geo = geocoder.description_for_number(parsed, "en")
    return geo.strip() if geo and geo.strip() else "Not Available"


def get_india_state(n):
    p = n[:4]
    m = {
        # ── Delhi ──────────────────────────────────
        "9810": "Delhi",          "9811": "Delhi",          "9871": "Delhi",
        "9870": "Delhi",          "9910": "Delhi",          "9990": "Delhi",
        "9999": "Delhi",          "9540": "Delhi",          "8800": "Delhi",
        "7011": "Delhi",          "7042": "Delhi",          "7043": "Delhi",
        "7044": "Delhi",          "7045": "Delhi",          "9312": "Delhi",
        "9717": "Delhi",          "9716": "Delhi",          "9313": "Delhi",

        # ── Maharashtra ────────────────────────────
        "9820": "Maharashtra",    "9821": "Maharashtra",    "9822": "Maharashtra",
        "9823": "Maharashtra",    "9850": "Maharashtra",    "9860": "Maharashtra",
        "9890": "Maharashtra",    "9920": "Maharashtra",    "9930": "Maharashtra",
        "9960": "Maharashtra",    "9970": "Maharashtra",    "9503": "Maharashtra",
        "9527": "Maharashtra",    "9545": "Maharashtra",    "7020": "Maharashtra",
        "7021": "Maharashtra",    "8390": "Maharashtra",    "9167": "Maharashtra",
        "9004": "Maharashtra",    "9326": "Maharashtra",    "9373": "Maharashtra",

        # ── Karnataka ──────────────────────────────
        "9845": "Karnataka",      "9880": "Karnataka",      "9900": "Karnataka",
        "9980": "Karnataka",      "9448": "Karnataka",      "9449": "Karnataka",
        "9480": "Karnataka",      "9481": "Karnataka",      "9482": "Karnataka",
        "9513": "Karnataka",      "9535": "Karnataka",      "6360": "Karnataka",
        "7022": "Karnataka",      "8050": "Karnataka",      "9972": "Karnataka",
        "9886": "Karnataka",      "9342": "Karnataka",      "7019": "Karnataka",

        # ── Tamil Nadu ─────────────────────────────
        "9840": "Tamil Nadu",     "9940": "Tamil Nadu",     "9443": "Tamil Nadu",
        "9500": "Tamil Nadu",     "9514": "Tamil Nadu",     "9515": "Tamil Nadu",
        "9543": "Tamil Nadu",     "6380": "Tamil Nadu",     "7010": "Tamil Nadu",
        "8300": "Tamil Nadu",     "9444": "Tamil Nadu",     "9952": "Tamil Nadu",
        "9361": "Tamil Nadu",     "9894": "Tamil Nadu",     "8124": "Tamil Nadu",

        # ── Kerala ─────────────────────────────────
        "9400": "Kerala",         "9446": "Kerala",         "9447": "Kerala",
        "9495": "Kerala",         "9496": "Kerala",         "9539": "Kerala",
        "9544": "Kerala",         "9895": "Kerala",         "8281": "Kerala",
        "9387": "Kerala",         "7994": "Kerala",
        "8086": "Kerala",         "9048": "Kerala",

        # ── Uttar Pradesh ──────────────────────────
        "9801": "Uttar Pradesh",  "9450": "Uttar Pradesh",  "9451": "Uttar Pradesh",
        "9452": "Uttar Pradesh",  "9506": "Uttar Pradesh",  "9511": "Uttar Pradesh",
        "9516": "Uttar Pradesh",  "9517": "Uttar Pradesh",  "9518": "Uttar Pradesh",
        "9519": "Uttar Pradesh",  "9520": "Uttar Pradesh",  "9521": "Uttar Pradesh",
        "9522": "Uttar Pradesh",  "9523": "Uttar Pradesh",  "9528": "Uttar Pradesh",
        "9532": "Uttar Pradesh",  "9536": "Uttar Pradesh",  "9538": "Uttar Pradesh",
        "9548": "Uttar Pradesh",  "9455": "Uttar Pradesh",  "9415": "Uttar Pradesh",
        "9616": "Uttar Pradesh",  "9617": "Uttar Pradesh",  "9618": "Uttar Pradesh",
        "9619": "Uttar Pradesh",  "9554": "Uttar Pradesh",  "9555": "Uttar Pradesh",
        "9557": "Uttar Pradesh",  "9670": "Uttar Pradesh",  "9671": "Uttar Pradesh",
        "9336": "Uttar Pradesh",  "9335": "Uttar Pradesh",  "9305": "Uttar Pradesh",
        "9307": "Uttar Pradesh",  "9198": "Uttar Pradesh",  "9369": "Uttar Pradesh",
        "8887": "Uttar Pradesh",  "8858": "Uttar Pradesh",  "8601": "Uttar Pradesh",
        "8756": "Uttar Pradesh",  "7500": "Uttar Pradesh",  "7800": "Uttar Pradesh",
        "8400": "Uttar Pradesh",  "9792": "Uttar Pradesh",  "9793": "Uttar Pradesh",
        "9795": "Uttar Pradesh",  "9026": "Uttar Pradesh",

        # ── Rajasthan ──────────────────────────────
        "9950": "Rajasthan",      "9460": "Rajasthan",      "9461": "Rajasthan",
        "9462": "Rajasthan",      "9504": "Rajasthan",      "9509": "Rajasthan",
        "9524": "Rajasthan",      "9529": "Rajasthan",      "9530": "Rajasthan",
        "9531": "Rajasthan",      "9549": "Rajasthan",      "7400": "Rajasthan",
        "7450": "Rajasthan",      "7451": "Rajasthan",      "7452": "Rajasthan",
        "7453": "Rajasthan",      "7454": "Rajasthan",      "7455": "Rajasthan",
        "7456": "Rajasthan",      "7457": "Rajasthan",      "7458": "Rajasthan",
        "7459": "Rajasthan",      "7460": "Rajasthan",      "7900": "Rajasthan",
        "9414": "Rajasthan",      "9413": "Rajasthan",      "9928": "Rajasthan",
        "9929": "Rajasthan",      "8058": "Rajasthan",      "7737": "Rajasthan",

        # ── Gujarat ────────────────────────────────
        "9510": "Gujarat",        "9512": "Gujarat",        "9537": "Gujarat",
        "7600": "Gujarat",        "8000": "Gujarat",        "8200": "Gujarat",
        "9099": "Gujarat",        "9898": "Gujarat",        "9427": "Gujarat",
        "9909": "Gujarat",        "9824": "Gujarat",        "9825": "Gujarat",
        "9979": "Gujarat",        "8140": "Gujarat",

        # ── Punjab ─────────────────────────────────
        "9803": "Punjab",         "9876": "Punjab",         "9501": "Punjab",
        "7700": "Punjab",         "9779": "Punjab",         "9814": "Punjab",
        "9815": "Punjab",         "9417": "Punjab",         "8146": "Punjab",
        "9878": "Punjab",         "7087": "Punjab",

        # ── Haryana ────────────────────────────────
        "9502": "Haryana",        "9525": "Haryana",        "9526": "Haryana",
        "9812": "Haryana",        "9813": "Haryana",        "9896": "Haryana",
        "8901": "Haryana",        "7015": "Haryana",        "9416": "Haryana",

        # ── West Bengal ────────────────────────────
        "9800": "West Bengal",    "9830": "West Bengal",    "9474": "West Bengal",
        "9475": "West Bengal",    "9547": "West Bengal",    "7001": "West Bengal",
        "8100": "West Bengal",    "9433": "West Bengal",    "9831": "West Bengal",
        "8697": "West Bengal",

        # ── Andhra Pradesh ─────────────────────────
        "9490": "Andhra Pradesh", "9491": "Andhra Pradesh", "9505": "Andhra Pradesh",
        "9533": "Andhra Pradesh", "9542": "Andhra Pradesh", "9550": "Andhra Pradesh",
        "8500": "Andhra Pradesh", "9848": "Andhra Pradesh",
        "8179": "Andhra Pradesh", "7093": "Andhra Pradesh",

        # ── Telangana ──────────────────────────────
        "9492": "Telangana",      "9494": "Telangana",      "9000": "Telangana",
        "9849": "Telangana",      "7386": "Telangana",      "8801": "Telangana",
        "9010": "Telangana",      "9100": "Telangana",

        # ── Bihar ──────────────────────────────────
        "9472": "Bihar",          "9473": "Bihar",          "9507": "Bihar",
        "9534": "Bihar",          "6200": "Bihar",          "6300": "Bihar",
        "9006": "Bihar",          "7546": "Bihar",          "8544": "Bihar",
        "9304": "Bihar",          "9199": "Bihar",

        # ── Jharkhand ──────────────────────────────
        "9470": "Jharkhand",      "9471": "Jharkhand",      "9508": "Jharkhand",
        "9546": "Jharkhand",      "8986": "Jharkhand",      "7488": "Jharkhand",

        # ── Odisha ─────────────────────────────────
        "8700": "Odisha",         "6370": "Odisha",         "9937": "Odisha",
        "7894": "Odisha",         "9438": "Odisha",         "8895": "Odisha",

        # ── Assam ──────────────────────────────────
        "8900": "Assam",          "6000": "Assam",          "9954": "Assam",
        "9435": "Assam",          "8638": "Assam",          "7002": "Assam",

        # ── Madhya Pradesh ─────────────────────────
        "7000": "Madhya Pradesh", "9926": "Madhya Pradesh", "9425": "Madhya Pradesh",
        "8109": "Madhya Pradesh", "7693": "Madhya Pradesh", "9981": "Madhya Pradesh",
        "8878": "Madhya Pradesh", "7697": "Madhya Pradesh",

        # ── Himachal Pradesh ───────────────────────
        "9802": "Himachal Pradesh", "9816": "Himachal Pradesh", "9817": "Himachal Pradesh",
        "9418": "Himachal Pradesh", "8894": "Himachal Pradesh",

        # ── Uttarakhand ────────────────────────────
        "9541": "Uttarakhand",    "9410": "Uttarakhand",    "7060": "Uttarakhand",
        "8979": "Uttarakhand",

        # ── Goa ────────────────────────────────────
        "7798": "Goa",            "9881": "Goa",            "8322": "Goa",

        # ── Chhattisgarh ───────────────────────────
        "9770": "Chhattisgarh",   "7415": "Chhattisgarh",   "9752": "Chhattisgarh",
        "8889": "Chhattisgarh",

        # ── Jammu & Kashmir ────────────────────────
        "9419": "Jammu & Kashmir", "9469": "Jammu & Kashmir", "7006": "Jammu & Kashmir",
        "9596": "Jammu & Kashmir", "8491": "Jammu & Kashmir",

        # ── North East States ──────────────────────
        "9862": "Nagaland",       "9856": "Manipur",        "9436": "Manipur",
        "9612": "Mizoram",        "9863": "Meghalaya",      "9402": "Nagaland",
        "8414": "Tripura",        "9774": "Tripura",        "9403": "Arunachal Pradesh",

        # ── Rajasthan extra ────────────────────────
        "9660": "Rajasthan",      "9694": "Rajasthan",      "9166": "Rajasthan",
    }
    return m.get(p, "Not Available")


# ══════════════════════════════════════════════════════════════
#  PUBLIC CHECKS  (no API key needed)
# ══════════════════════════════════════════════════════════════

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def check_whatsapp(e164):
    """
    Probe wa.me to check WhatsApp registration.
    Checks page content — NOT the URL (URL always redirects away from wa.me).
    Registered   --> page has "send message", "open whatsapp" etc.
    Unregistered --> page has "phone number shared via link is not"
    """
    print(Fore.CYAN + "  [~] WhatsApp    : Probing...", end="", flush=True)
    try:
        clean = e164.replace("+", "")
        r = requests.get(
            f"https://wa.me/{clean}",
            headers=HEADERS, timeout=10, allow_redirects=True
        )
        content = r.text.lower()

        not_registered_signals = [
            "phone number shared via link is not",
            "number is not registered",
            "invalid phone number",
            "this phone number is not on whatsapp",
            "not on whatsapp",
        ]
        registered_signals = [
            "send message",
            "open whatsapp",
            "continue to chat",
            "chat with",
            "whatsapp.com/send",
            "api.whatsapp.com",
        ]

        for sig in not_registered_signals:
            if sig in content:
                print(Fore.RED + " NOT REGISTERED")
                return "Not Registered  [-]"

        for sig in registered_signals:
            if sig in content:
                print(Fore.GREEN + " REGISTERED")
                return "Registered  [+]"

        # Page loaded with no error signal -- likely registered
        if r.status_code == 200:
            print(Fore.GREEN + " LIKELY REGISTERED")
            return "Likely Registered  [+]"

        print(Fore.YELLOW + " INCONCLUSIVE")
        return "Inconclusive"

    except requests.exceptions.Timeout:
        print(Fore.YELLOW + " TIMEOUT")
        return "Timed Out"
    except Exception:
        print(Fore.RED + " FAILED")
        return "Check Failed"


def _parse_spam_page(text, url):
    """Parse spam rating from scraped page content."""
    t = text.lower()
    if "dangerous" in t or "scam" in t or "fraud" in t or "harassing" in t:
        return {"rating": "DANGEROUS / SCAM REPORTED  [!!]", "url": url}
    elif "spam" in t or "unwanted" in t or "telemarketing" in t:
        return {"rating": "Spam Reported  [!]", "url": url}
    elif "safe" in t or "positive" in t or "no complaints" in t:
        return {"rating": "Safe  [OK]", "url": url}
    elif "neutral" in t:
        return {"rating": "Neutral  (no strong reports)", "url": url}
    else:
        return {"rating": "No Reports Found", "url": url}


def check_spam(e164):
    """
    Try multiple public spam databases in order.
    Moves to next source if one fails or returns no useful data.
    """
    print(Fore.CYAN + "  [~] Spam Check  : Scraping...", end="", flush=True)

    clean = e164.replace("+", "")

    sources = [
        {
            "name": "NumLookup",
            "url" : f"https://www.numlookup.com/results?phone={e164}",
        },
        {
            "name": "ShouldIAnswer",
            "url" : f"https://www.shouldianswer.com/phone-number/{clean}",
        },
        {
            "name": "WhoCalledMe",
            "url" : f"https://www.whocalledme.com/PhoneNumber/{clean}",
        },
    ]

    for source in sources:
        try:
            r = requests.get(source["url"], headers=HEADERS, timeout=10)
            # Only process if page loaded properly with meaningful content
            if r.status_code == 200 and len(r.text) > 500:
                result = _parse_spam_page(r.text, source["url"])
                result["source"] = source["name"]
                color = (
                    Fore.RED    if "[!!]" in result["rating"] or "[!]" in result["rating"]
                    else Fore.GREEN  if "[OK]" in result["rating"]
                    else Fore.YELLOW
                )
                print(color + f" {result['rating'].split('[')[0].strip()}")
                return result
        except Exception:
            continue

    print(Fore.YELLOW + " NO DATA")
    return None


# ══════════════════════════════════════════════════════════════
#  CORE ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_number(number, save=False):
    # ── Parse number ──
    try:
        parsed = phonenumbers.parse(number, None)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(Fore.RED    + f"\n  [!] Cannot parse number: {e}")
        print(Fore.YELLOW + "      Always include country code.")
        print(Fore.YELLOW + "      Example: +919876543210  |  +14155552671")
        return

    # ── Validate ──
    if not is_valid_number(parsed):
        print(Fore.RED    + "\n  [!] Invalid phone number.")
        print(Fore.YELLOW + "      Check the number and country code, then try again.")
        return

    loading_bar("Analyzing number")

    # ── Extract all data from phonenumbers library ──
    country      = geocoder.description_for_number(parsed, "en") or "Not Available"
    sim_carrier  = carrier.name_for_number(parsed, "en")         or "Not Available"
    sim_type_int = number_type(parsed)
    time_zones   = timezone.time_zones_for_number(parsed)
    country_code = parsed.country_code
    national_num = str(parsed.national_number)
    region_code  = region_code_for_number(parsed)
    possible     = is_possible_number(parsed)

    # ── Number formats ──
    intl_fmt = format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
    natl_fmt = format_number(parsed, PhoneNumberFormat.NATIONAL)
    e164_fmt = format_number(parsed, PhoneNumberFormat.E164)
    rfc_fmt  = format_number(parsed, PhoneNumberFormat.RFC3966)

    # ── Derived info ──
    region_area  = get_region(parsed, national_num)
    phone_type   = get_phone_type_str(sim_type_int)
    sim_type_str = get_sim_type(sim_type_int)
    call_type    = get_call_type(parsed)
    is_mobile    = sim_type_int == 1
    is_tollfree  = sim_type_int == 3
    is_voip      = sim_type_int == 6

    # ── Public checks ──
    print(Fore.CYAN + "  [*] Running public checks...\n")
    wa_status = check_whatsapp(e164_fmt)
    spam_data = check_spam(e164_fmt)

    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    SEP = "=" * 60

    # ── Build report lines ──
    lines = [
        SEP,
        "  PhoneXtract v3.0  --  Number Intelligence Report",
        f"  Generated        : {ts}",
        f"  Target Number    : {number}",
        SEP,
        "",
        "  -- IDENTIFICATION " + "-" * 41,
        f"  International    : {intl_fmt}",
        f"  National Format  : {natl_fmt}",
        f"  E164 Format      : {e164_fmt}",
        f"  RFC3966 Format   : {rfc_fmt}",
        f"  Valid Number     : Yes",
        f"  Possible Number  : {'Yes' if possible else 'No'}",
        "",
        "  -- LOCATION " + "-" * 47,
        f"  Country          : {country}",
        f"  Region / State   : {region_area}",
        f"  Country Code     : +{country_code}",
        f"  Region Code      : {region_code}",
        f"  Time Zone        : {', '.join(time_zones) if time_zones else 'Not Available'}",
        "",
        "  -- CARRIER & LINE " + "-" * 41,
        f"  Carrier          : {sim_carrier}",
        f"  Phone Type       : {phone_type}",
        f"  SIM Category     : {sim_type_str}",
        f"  Call Type        : {call_type}",
        f"  Mobile Number    : {'Yes' if is_mobile else 'No'}",
        f"  Toll Free        : {'Yes' if is_tollfree else 'No'}",
        f"  VoIP / Internet  : {'Yes' if is_voip else 'No'}",
        "",
        "  -- NUMBER DETAILS " + "-" * 41,
        f"  Number Length    : {len(national_num)} digits",
        f"  Area Code        : {national_num[:3]}",
        f"  Subscriber No.   : {national_num[3:]}",
        f"  Prefix (4-digit) : {national_num[:4]}",
        "",
        "  -- SOCIAL MEDIA " + "-" * 43,
        f"  WhatsApp         : {wa_status}",
        "",
        "  -- SPAM REPUTATION " + "-" * 40,
    ]

    if spam_data:
        lines += [
            f"  Rating           : {spam_data.get('rating', 'N/A')}",
            f"  Data Source      : {spam_data.get('source', 'N/A')}",
            f"  Source URL       : {spam_data.get('url', 'N/A')}",
        ]
    else:
        lines += [
            "  Rating           : Could not fetch  (all sources unavailable)",
            "  Data Source      : N/A",
        ]

    lines += [
        "",
        "  -- NOTE " + "-" * 51,
        "  [!] Carrier is prefix-based. May differ if number",
        "      was ported to another carrier (MNP).",
        "  [!] Region/State is prefix-based, not real-time GPS.",
        "  [!] WhatsApp check is best-effort only.",
        "  [!] All data from public records. No API key used.",
        SEP,
        "  PhoneXtract v3.0  by Alok Thakur  |  Firewall Breaker",
        SEP,
    ]

    report_text = "\n".join(lines)

    # ── Print with colors ──
    print()
    for ln in lines:
        s = ln.strip()
        if s.startswith("="):
            print(Fore.GREEN + ln)
        elif s.startswith("-- "):
            print(Fore.CYAN + ln)
        elif "[!!]" in ln or "DANGEROUS" in ln or "SCAM" in ln:
            print(Fore.RED + ln)
        elif "[!]" in ln and not s.startswith("[!]"):
            print(Fore.RED + ln)
        elif "[+]" in ln or "[OK]" in ln or "Safe" in ln:
            print(Fore.GREEN + ln)
        elif "[-]" in ln or "Not Registered" in ln:
            print(Fore.RED + ln)
        elif s.startswith("[!]"):
            print(Fore.YELLOW + ln)
        elif s.startswith("PhoneXtract v3"):
            print(Fore.MAGENTA + ln)
        else:
            print(Fore.WHITE + ln)

    if save:
        save_report(report_text, number)


# ══════════════════════════════════════════════════════════════
#  BATCH MODE
# ══════════════════════════════════════════════════════════════

def batch_mode():
    print(Fore.CYAN   + "\n  [*] Batch Mode")
    print(Fore.YELLOW + "  One number per line with country code.")
    print(Fore.YELLOW + "  Lines starting with # are ignored (comments).")
    print(Fore.YELLOW + "  Example:  +919876543210\n")

    filepath = input(Fore.CYAN + "  [>] Path to .txt file: ").strip()

    if not os.path.exists(filepath):
        print(Fore.RED + "  [!] File not found. Check the path and try again.")
        return

    with open(filepath, "r") as f:
        numbers = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    if not numbers:
        print(Fore.RED + "  [!] No valid numbers found in file.")
        return

    print(Fore.GREEN + f"\n  [+] {len(numbers)} number(s) loaded.")
    save_all = input(Fore.CYAN + "  [?] Save individual reports? (Y/N): ").strip().lower() == 'y'

    for i, num in enumerate(numbers, 1):
        print(Fore.YELLOW + f"\n  [{i}/{len(numbers)}] ---- Target: {num} ----")
        analyze_number(num, save=save_all)
        if i < len(numbers):
            time.sleep(1.5)  # Polite delay between requests

    print(Fore.GREEN + f"\n  [+] Batch complete. {len(numbers)} numbers analyzed.")


# ══════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════

def main_menu():
    while True:
        clear_screen()
        banner()

        print(Fore.CYAN + "\n  Select an option:\n")
        print(Fore.WHITE + "  [1]  Single Number Analysis")
        print(Fore.WHITE + "  [2]  Batch Mode  (multiple numbers from .txt file)")
        print(Fore.WHITE + "  [3]  About / Help")
        print(Fore.RED   + "  [0]  Exit\n")

        choice = input(Fore.CYAN + "  [>] Enter choice: ").strip()

        if choice == "1":
            print()
            print(Fore.YELLOW + "  Enter number with country code.\n")
            print(Fore.WHITE  + "  +-----------+------------------------+")
            print(Fore.WHITE  + "  | Country   | Example                |")
            print(Fore.WHITE  + "  +-----------+------------------------+")
            print(Fore.WHITE  + "  | India     | +919876543210          |")
            print(Fore.WHITE  + "  | USA       | +14155552671           |")
            print(Fore.WHITE  + "  | UK        | +447911123456          |")
            print(Fore.WHITE  + "  | UAE       | +971501234567          |")
            print(Fore.WHITE  + "  | Germany   | +4915123456789         |")
            print(Fore.WHITE  + "  | Australia | +61412345678           |")
            print(Fore.WHITE  + "  +-----------+------------------------+\n")

            num = input(Fore.CYAN + "  [>] Phone number: ").strip()
            if not num:
                print(Fore.RED + "\n  [!] No input provided.")
                time.sleep(1)
                continue

            save = input(Fore.CYAN + "  [?] Save report to .txt? (Y/N): ").strip().lower() == 'y'
            analyze_number(num, save=save)
            input(Fore.CYAN + "\n  [>] Press Enter to return to menu...")

        elif choice == "2":
            batch_mode()
            input(Fore.CYAN + "\n  [>] Press Enter to return to menu...")

        elif choice == "3":
            clear_screen()
            banner()
            print(Fore.CYAN + """
  PhoneXtract v3.0  --  Number Intelligence Tool
  ================================================

  WHAT IT SHOWS:
  [+] Country, Region / State, Time Zone
  [+] Carrier name  (prefix-based)
  [+] Phone type    (Mobile / Fixed / VoIP etc.)
  [+] SIM category  (Prepaid / Postpaid estimate)
  [+] All formats   (International / National / E164 / RFC3966)
  [+] Number length, Area code, Subscriber no., Prefix
  [+] WhatsApp registration check
  [+] Spam reputation  (3 sources tried automatically)
  [+] Batch mode  -- analyze multiple numbers at once
  [+] Save full report to .txt file

  SUPPORTED COUNTRIES:
  Works with all countries worldwide.
  Region/State detection optimized for India (250+ prefixes).
  Other countries use geocoder data where available.

  NO API KEY REQUIRED -- 100% free to use.

  ACCURACY NOTE:
  [!] Carrier may differ due to number porting (MNP).
  [!] Region is NOT real-time GPS location.
  [!] WhatsApp check is best-effort only.
  [!] Spam check scrapes public websites.
            """)
            input(Fore.CYAN + "  [>] Press Enter to go back...")

        elif choice == "0":
            print(Fore.GREEN  + "\n  [+] Exiting PhoneXtract. Stay ethical.\n")
            print(Fore.MAGENTA+ "      Created by Alok Thakur | Firewall Breaker\n")
            break

        else:
            print(Fore.RED + "\n  [!] Invalid option. Enter 0, 1, 2 or 3.")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
