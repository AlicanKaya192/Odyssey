import re

PATTERNS = {
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "PHONE": r"\+?\(?\d[\d\s()-]{8,}\d",
    "ORDER": r"ORD-\d{5}",
}


def mask(text):
    for label, pattern in PATTERNS.items():
        text = re.sub(pattern, f"[{label}]", text)
    return text


for text in ["My number is (555) 123-4567.", "Mail ana.k@example.com", "Order ORD-48213"]:
    print(mask(text))
