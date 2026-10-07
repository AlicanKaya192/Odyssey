VERBS = ["get", "create", "update", "delete", "remove", "add"]


def check_endpoint(method, path):
    pieces = [piece for piece in path.split("/") if piece]
    for piece in pieces:
        for verb in VERBS:
            if piece.lower().startswith(verb):
                return "verb in path"
    return "ok"


endpoints = [
    ("GET", "/books"),
    ("GET", "/getBooks"),
    ("POST", "/books/42/delete"),
    ("DELETE", "/books/42"),
    ("POST", "/createBook"),
    ("GET", "/authors/6/books"),
    ("PATCH", "/books/42"),
]
for method, path in endpoints:
    print(method, path, "->", check_endpoint(method, path))
