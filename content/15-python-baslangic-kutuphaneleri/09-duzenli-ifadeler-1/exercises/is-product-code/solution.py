import re


def is_product_code(code):
    return re.fullmatch(r"[A-Z]{2}-\d{4}", code) is not None

for code in ["AB-1234", "ab-1234", "AB-123", "XAB-1234"]:
    print(code, is_product_code(code))
