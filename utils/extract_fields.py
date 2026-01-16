import re

def clean_text(text):
    return text.replace(",", "").replace(" ", "").upper()


def clean_model_name(model):
    if not model:
        return None

    noise = ["COST OF", "TRACTOR", "MODEL", ":-"]
    model = model.upper()

    for n in noise:
        model = model.replace(n, "")

    return model.strip()


def extract_model_name(ocr_results):
    """
    Improved heuristic for tractor model:
    - Must contain brand or tractor-related keywords
    - Must contain digits (model numbers)
    - Must NOT contain legal / warranty language
    """

    NEGATIVE_KEYWORDS = [
        "WARRANTY", "PRICE", "DELIVERY", "BANK",
        "ISSUE", "LETTER", "TERMS", "SUBJECT",
        "TRANSACTION", "PAYMENT"
    ]

    POSITIVE_KEYWORDS = [
        "TRACTOR", "SWARAJ", "MAHINDRA", "SONALIKA",
        "EICHER", "JOHN", "DEERE", "POWERTRAC",
        "FARMTRAC", "KUBOTA", "DI", "FE", "4WD"
    ]

    candidates = []

    for r in ocr_results:
        text = r["text"].upper()

        # Skip legal / irrelevant lines
        if any(neg in text for neg in NEGATIVE_KEYWORDS):
            continue

        # Must contain a digit (model number)
        if not any(ch.isdigit() for ch in text):
            continue

        # Must contain a positive keyword
        if any(pos in text for pos in POSITIVE_KEYWORDS):
            if len(text) > 8:
                candidates.append(text)

    if not candidates:
        return None

    # Prefer medium-length informative lines
    candidates.sort(key=len)
    return candidates[0]


def extract_horse_power(ocr_results):
    # 1. First pass: look for explicit HP
    for r in ocr_results:
        text = r["text"].upper()

        # Normalize OCR: O -> 0
        text = text.replace("O", "0").replace(" ", "")

        match = re.search(r"(\d{2,3})HP", text)
        if match:
            hp = int(match.group(1))
            if 20 <= hp <= 120:
                return hp

    # 2. Second pass: fallback like H8 -> 48
    for r in ocr_results:
        text = r["text"].upper().replace(" ", "")
        match = re.search(r"H(\d)", text)
        if match:
            return 40 + int(match.group(1))

    return None


def extract_asset_cost(ocr_results):
    """
    Heuristic:
    - Extract all numbers
    - Pick largest reasonable value
    """
    numbers = []

    for r in ocr_results:
        text = r["text"].replace(",", "").replace(" ", "")
        matches = re.findall(r"\d{5,7}", text)
        for m in matches:
            val = int(m)
            if 50000 <= val <= 2000000:
                numbers.append(val)

    if not numbers:
        return None

    return max(numbers)


def extract_dealer_name(ocr_results):
    LEGAL_TERMS = [
        "LTD", "LIMITED", "PVT", "CORPORATION",
        "COMPANY", "CO.", "MOTORS", "TRACTORS", "AGRO"
    ]

    BAD_KEYWORDS = [
        "PIN", "MAIL", "EMAIL", "E-MAIL",
        "PHONE", "PH:", "FAX",
        "NOTE", "N.B", "COMMITTEE", "PURCHASE",
        "SELLING", "PRICE", "TERMS", "CONDITIONS",
        "DIFFERENT MAKE", "MODELS OF"
    ]

    candidates = []

    for r in ocr_results[:30]:
        text = r["text"].upper().strip()

        if len(text) < 10:
            continue

        # reject obvious bad lines
        if any(bad in text for bad in BAD_KEYWORDS):
            continue

        # must contain legal organisation term
        if not any(term in text for term in LEGAL_TERMS):
            continue

        candidates.append(text)

    if not candidates:
        return None

    # choose longest valid organisation name
    dealer = max(candidates, key=len)

    # hard cut after legal suffix
    for suffix in [" LTD", " LIMITED", " PVT", " CORPORATION", " MOTORS", " TRACTORS"]:
        if suffix in dealer:
            dealer = dealer.split(suffix)[0] + suffix
            break

    return dealer.strip()
