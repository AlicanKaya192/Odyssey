REQUIRED = [
    "content-security-policy",
    "strict-transport-security",
    "x-content-type-options",
    "referrer-policy",
    "x-frame-options",
]


def missing_headers(headers):
    return [name for name in REQUIRED if name not in headers]

response = {
    "content-type": "text/html",
    "X-Frame-Options": "DENY",
    "REFERRER-POLICY": "no-referrer",
}
for name in missing_headers(response):
    print(name)
