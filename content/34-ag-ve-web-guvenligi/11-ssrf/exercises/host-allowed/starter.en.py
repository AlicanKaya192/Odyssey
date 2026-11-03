from urllib.parse import urlsplit


def allowed(url, hosts):
    return any(url.startswith("https://" + h) for h in hosts)

HOSTS = ["images.example.com"]
for url in ["https://images.example.com/cat.png",
            "http://127.0.0.1/admin",
            "https://images.example.com@127.0.0.1/",
            "file:///app/settings.ini"]:
    print(allowed(url, HOSTS))
