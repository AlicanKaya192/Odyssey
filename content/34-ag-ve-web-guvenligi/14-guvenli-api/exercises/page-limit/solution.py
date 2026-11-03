import re


def page_limit(value):
    if value is None or not re.fullmatch(r"[0-9]{1,6}", value):
        return 20
    return max(1, min(100, int(value)))

for value in [None, "50", "0", "500", "ten", "-5"]:
    print(repr(value), page_limit(value))
