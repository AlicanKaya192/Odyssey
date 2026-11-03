from urllib.parse import urlsplit


def ok(url, hosts):
    parts = urlsplit(url)
    return parts.scheme in ("http", "https") and parts.hostname in hosts


def first_bad(chain, hosts):
    for i, url in enumerate(chain):
        if not ok(url, hosts):
            return i
    return -1

HOSTS = ["images.example.com", "cdn.example.com"]
chain = ["https://images.example.com/a", "https://cdn.example.com/b",
         "http://127.0.0.1/admin"]
print(first_bad(chain, HOSTS))
print(first_bad(chain[:2], HOSTS))
