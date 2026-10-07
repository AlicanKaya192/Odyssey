import os

import requests

BASE = "http://api.odyssey.test"

token = os.environ.get("LIBRARY_TOKEN", "letmein")
session = requests.Session()
session.headers.update({"Authorization": "Bearer " + token})

book = {"title": "The Word for World Is Forest", "price": 11.5, "author_id": 6}
r = session.post(BASE + "/books", json=book, timeout=10)
location = r.headers["Location"]
print("created:", r.status_code, location)

r = session.patch(BASE + location, json={"price": 9.99}, timeout=10)
print("patched:", r.status_code)

book = session.get(BASE + location, timeout=10).json()
print(book["title"], book["author"]["name"], book["price"])
