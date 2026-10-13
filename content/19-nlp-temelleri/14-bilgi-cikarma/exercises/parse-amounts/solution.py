import re


def parse_amounts(text):
    values = []
    for match in re.findall(r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", text):
        values.append(round(float(match.replace(",", "")), 2))
    return values

print(parse_amounts("Paid $1,200.00, refunded $5 and $12.49."))
print(parse_amounts("No money here: 2.49"))
