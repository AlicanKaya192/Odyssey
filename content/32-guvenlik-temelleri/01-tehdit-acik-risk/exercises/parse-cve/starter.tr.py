def parse_cve(text):
    # parcalara bol, her kurali denetle
    return None

for text in ["CVE-2025-12345", " cve-2019-0042 ", "CVE-25-1234", "CVE-2024-12a4"]:
    print(repr(text), parse_cve(text))
