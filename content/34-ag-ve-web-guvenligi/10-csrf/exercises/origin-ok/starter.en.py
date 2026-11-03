from urllib.parse import urlsplit


def origin_ok(headers, allowed):
    return headers.get("origin") in allowed

ALLOWED = ["https://bank.example"]
print(origin_ok({"origin": "https://bank.example"}, ALLOWED))
print(origin_ok({"origin": "https://games.example"}, ALLOWED))
print(origin_ok({"referer": "https://bank.example/pay?x=1"}, ALLOWED))
print(origin_ok({}, ALLOWED))
