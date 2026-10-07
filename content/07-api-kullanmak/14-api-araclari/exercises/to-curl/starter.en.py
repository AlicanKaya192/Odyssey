# to_curl(method, url, headers): a curl command (text)


samples = [
    ("GET", "https://api.example.com/books", {}),
    ("GET", "https://api.example.com/stats", {"X-API-Key": "abc"}),
    ("DELETE", "https://api.example.com/books/7", {"Authorization": "Bearer abc"}),
]
