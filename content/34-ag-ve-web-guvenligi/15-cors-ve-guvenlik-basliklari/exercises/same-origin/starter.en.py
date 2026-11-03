from urllib.parse import urlsplit

DEFAULT_PORTS = {"http": 80, "https": 443}


def same_origin(a, b):
    return a == b

base = "https://shop.example"
for other in [
    "https://shop.example:443/a",
    "http://shop.example",
    "https://api.shop.example",
    "https://SHOP.example/b",
]:
    print(same_origin(base, other))
