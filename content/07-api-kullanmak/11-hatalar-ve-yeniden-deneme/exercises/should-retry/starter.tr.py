# should_retry(method, outcome): True ya da False


cases = [
    ("GET", 503),
    ("GET", 404),
    ("get", "timeout"),
    ("POST", 503),
    ("DELETE", "connection"),
    ("PUT", 429),
    ("GET", 200),
    ("patch", 500),
]
# Her durum icin: "GET 503 -> True"
