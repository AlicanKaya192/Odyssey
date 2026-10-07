IDEMPOTENT = ["GET", "HEAD", "OPTIONS", "PUT", "DELETE"]


def can_retry(method):
    return method.upper() in IDEMPOTENT


failed = [
    ("GET", "/books"),
    ("POST", "/orders"),
    ("DELETE", "/books/7"),
    ("patch", "/books/7"),
    ("PUT", "/books/7"),
]
for method, path in failed:
    if can_retry(method):
        print("retry", method.upper(), path)
    else:
        print("ask first", method.upper(), path)
