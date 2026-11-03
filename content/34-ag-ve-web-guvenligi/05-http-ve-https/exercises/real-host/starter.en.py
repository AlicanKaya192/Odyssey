from urllib.parse import urlsplit


def real_host(url):
    parts = url.split("/")
    if len(parts) < 3:
        return ""
    return parts[2].lower()

for url in ["https://shop.example.com/cart",
            "https://shop.example.com@203.0.113.66/",
            "HTTPS://Shop.Example.com/x",
            "not a url"]:
    print(repr(real_host(url)))
