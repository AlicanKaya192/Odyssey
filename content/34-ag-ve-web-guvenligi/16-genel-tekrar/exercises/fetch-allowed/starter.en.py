from urllib.parse import urlsplit

ALLOWED_HOSTS = {"images.example", "cdn.images.example"}


def fetch_allowed(url):
    return "images.example" in url

for url in [
    "https://images.example/a.png",
    "ftp://images.example/a.png",
    "https://images.example.other.example/a",
    "https://IMAGES.example/a.png",
    "http://cdn.images.example:8080/a",
    "https://other.example/?u=images.example",
]:
    print(fetch_allowed(url))
