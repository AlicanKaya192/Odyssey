import re

PATTERNS = {"EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
            "PHONE": r"\+?\(?\d[\d\s()-]{8,}\d",
            "ORDER": r"ORD-\d{5}"}


def mask_count(text):
    total = 0
    for label, pattern in PATTERNS.items():
        text, n = re.subn(pattern, f"[{label}]", text)
        total += n
    return [text, total]


print(mask_count("Mail ana@example.com, ORD-48213"))
