def parse_security_txt(text):
    fields = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        fields.setdefault(name.strip(), []).append(value.strip())
    return fields

TEXT = """# Contact: see below
Contact: mailto:security@example.org

Contact: https://example.org/report
Expires: 2026-12-31T23:59:59Z
"""
fields = parse_security_txt(TEXT)
for name in sorted(fields):
    print(name, len(fields[name]))
