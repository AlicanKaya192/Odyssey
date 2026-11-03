from urllib.parse import urlsplit


def origin_ok(headers, allowed):
    if "origin" in headers:
        return headers["origin"] in allowed
    if "referer" in headers:
        parts = urlsplit(headers["referer"])
        return parts.scheme + "://" + parts.netloc in allowed
    return False

ALLOWED = ["https://bank.example"]
print(origin_ok({"origin": "https://bank.example"}, ALLOWED))
print(origin_ok({"origin": "https://games.example"}, ALLOWED))
print(origin_ok({"referer": "https://bank.example/pay?x=1"}, ALLOWED))
print(origin_ok({}, ALLOWED))
