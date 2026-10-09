import re


def parse_date(text):
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", text)
    if m is None:
        return None
    day, month, year = m.groups()
    return int(year), int(month), int(day)

print(parse_date("Invoice 0042, due 15.03.2026, paid 20.03.2026"))
print(parse_date("no date"))
