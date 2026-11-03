from urllib.parse import urlsplit

DEFAULT_PORTS = {"http": 80, "https": 443}


def origin(url):
    parts = urlsplit(url)
    return parts.scheme, parts.hostname, parts.port or DEFAULT_PORTS[parts.scheme]


def same_origin(a, b):
    return origin(a) == origin(b)

base = "https://shop.example"
for other in [
    "https://shop.example:443/a",
    "http://shop.example",
    "https://api.shop.example",
    "https://SHOP.example/b",
]:
    print(same_origin(base, other))
