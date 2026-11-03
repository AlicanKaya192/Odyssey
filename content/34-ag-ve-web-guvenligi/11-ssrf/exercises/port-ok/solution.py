from urllib.parse import urlsplit

DEFAULTS = {"http": 80, "https": 443}


def port_ok(url):
    parts = urlsplit(url)
    if parts.scheme not in DEFAULTS:
        return False
    try:
        port = parts.port
    except ValueError:
        return False
    if port is None:
        port = DEFAULTS[parts.scheme]
    return port in (80, 443)

for url in ["https://images.example.com/", "http://images.example.com:8080/",
            "https://images.example.com:443/", "ftp://images.example.com/",
            "http://images.example.com:99999/"]:
    print(port_ok(url))
