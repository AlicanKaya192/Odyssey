import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}
CHANGE = {"title": "Changed", "price": 9.0}

# change_and_read(method, book_id): requests.request ile gonder, sonra GET ile oku


# 15'e PATCH, 14'e PUT: "PATCH Changed 9.0 1968 ['fantasy']"
