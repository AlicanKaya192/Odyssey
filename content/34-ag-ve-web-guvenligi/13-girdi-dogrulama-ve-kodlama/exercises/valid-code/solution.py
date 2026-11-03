import re


def valid_code(code):
    return re.fullmatch(r"[A-Z]{2}-[0-9]{4}", code) is not None

for code in ["AB-1234", "ab-1234", "AB-1234\n", "AB-12345"]:
    print(repr(code), valid_code(code))
