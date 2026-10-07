# can_retry(method): True for an idempotent method


failed = [
    ("GET", "/books"),
    ("POST", "/orders"),
    ("DELETE", "/books/7"),
    ("patch", "/books/7"),
    ("PUT", "/books/7"),
]
# For each request: "retry GET /books" or "ask first POST /orders"
