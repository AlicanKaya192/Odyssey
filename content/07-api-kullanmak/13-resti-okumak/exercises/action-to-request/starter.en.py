# to_request(action, book_id): a (method, address) tuple


jobs = [("list", None), ("read", 42), ("create", None), ("change", 7), ("remove", 3), ("replace", 9)]
# Each job: "change -> PATCH /books/7"
