import re


def parse_age(text):
    if not re.fullmatch(r"[0-9]{1,3}", text):
        return None
    value = int(text)
    if value > 150:
        return None
    return value

for text in ["42", "150", "151", "-3", "abc", ""]:
    print(repr(text), parse_age(text))
