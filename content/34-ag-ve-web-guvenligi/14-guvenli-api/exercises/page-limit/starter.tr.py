import re


def page_limit(value):
    return int(value)

for value in [None, "50", "0", "500", "ten", "-5"]:
    print(repr(value), page_limit(value))
