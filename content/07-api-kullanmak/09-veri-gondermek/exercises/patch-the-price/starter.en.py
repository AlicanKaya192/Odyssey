import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}

# 1) GET /books/12: "old price: ..."


# 2) PATCH /books/12 {"price": 5.5}: "patch: ..."


# 3) GET again: "new price: ...", "year: ..."
