import re


def hsts_ok(value):
    return "max-age" in value

for value in [
    "max-age=31536000; includeSubDomains",
    "max-age=600; includeSubDomains",
    "max-age=63072000",
    "Max-Age=31536000;includesubdomains",
    "max-age=abc; includeSubDomains",
]:
    print(hsts_ok(value))
