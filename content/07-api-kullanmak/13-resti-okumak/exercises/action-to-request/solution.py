METHODS = {"list": "GET", "read": "GET", "create": "POST",
           "replace": "PUT", "change": "PATCH", "remove": "DELETE"}


def to_request(action, book_id):
    method = METHODS[action]
    if book_id is None:
        return (method, "/books")
    return (method, "/books/" + str(book_id))


jobs = [("list", None), ("read", 42), ("create", None), ("change", 7), ("remove", 3), ("replace", 9)]
for action, book_id in jobs:
    method, path = to_request(action, book_id)
    print(action, "->", method, path)
