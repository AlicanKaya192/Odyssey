import re


def parse_date(text):
    # re.search + groups()
    return None

print(parse_date("Invoice 0042, due 15.03.2026, paid 20.03.2026"))
print(parse_date("no date"))
