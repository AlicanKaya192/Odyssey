# can_retry(method): tekrarlanabilir yontemse True


failed = [
    ("GET", "/books"),
    ("POST", "/orders"),
    ("DELETE", "/books/7"),
    ("patch", "/books/7"),
    ("PUT", "/books/7"),
]
# Her istek icin: "retry GET /books" ya da "ask first POST /orders"
