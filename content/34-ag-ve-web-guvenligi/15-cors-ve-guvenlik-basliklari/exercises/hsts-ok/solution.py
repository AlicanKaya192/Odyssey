import re


def hsts_ok(value):
    max_age = 0
    subdomains = False
    for part in value.split(";"):
        part = part.strip()
        name, _, number = part.partition("=")
        name = name.lower()
        if name == "max-age" and re.fullmatch(r"[0-9]+", number):
            max_age = int(number)
        elif name == "includesubdomains":
            subdomains = True
    return max_age >= 31536000 and subdomains

for value in [
    "max-age=31536000; includeSubDomains",
    "max-age=600; includeSubDomains",
    "max-age=63072000",
    "Max-Age=31536000;includesubdomains",
    "max-age=abc; includeSubDomains",
]:
    print(hsts_ok(value))
