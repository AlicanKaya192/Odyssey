VERBS = ["get", "create", "update", "delete", "remove", "add"]

# check_endpoint(method, path): "verb in path" ya da "ok"


endpoints = [
    ("GET", "/books"),
    ("GET", "/getBooks"),
    ("POST", "/books/42/delete"),
    ("DELETE", "/books/42"),
    ("POST", "/createBook"),
    ("GET", "/authors/6/books"),
    ("PATCH", "/books/42"),
]
# Her biri: "GET /getBooks -> verb in path"
