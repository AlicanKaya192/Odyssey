from urllib.parse import urlsplit

DEFAULTS = {"http": 80, "https": 443}


def port_ok(url):
    # semayi ve portu bul, varsayilani kullan
    return True

for url in ["https://images.example.com/", "http://images.example.com:8080/",
            "https://images.example.com:443/", "ftp://images.example.com/",
            "http://images.example.com:99999/"]:
    print(port_ok(url))
