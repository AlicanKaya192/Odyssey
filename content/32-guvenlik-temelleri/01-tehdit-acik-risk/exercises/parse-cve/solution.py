def parse_cve(text):
    parts = text.strip().upper().split("-")
    if len(parts) != 3 or parts[0] != "CVE":
        return None
    year, number = parts[1], parts[2]
    if len(year) != 4 or not year.isdigit() or int(year) < 1999:
        return None
    if len(number) < 4 or not number.isdigit():
        return None
    return (int(year), int(number))

for text in ["CVE-2025-12345", " cve-2019-0042 ", "CVE-25-1234", "CVE-2024-12a4"]:
    print(repr(text), parse_cve(text))
