def to_curl(method, url, headers):
    parts = ["curl"]
    if method != "GET":
        parts += ["-X", method]
    parts.append(url)
    for name, value in headers.items():
        parts.append('-H "' + name + ": " + value + '"')
    return " ".join(parts)


samples = [
    ("GET", "https://api.example.com/books", {}),
    ("GET", "https://api.example.com/stats", {"X-API-Key": "abc"}),
    ("DELETE", "https://api.example.com/books/7", {"Authorization": "Bearer abc"}),
]
for method, url, headers in samples:
    print(to_curl(method, url, headers))
