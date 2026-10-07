IDEMPOTENT = ["GET", "HEAD", "OPTIONS", "PUT", "DELETE"]


def should_retry(method, outcome):
    if method.upper() not in IDEMPOTENT:
        return False
    if outcome in ("timeout", "connection"):
        return True
    return outcome == 429 or outcome >= 500


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
for method, outcome in cases:
    print(method, outcome, "->", should_retry(method, outcome))
