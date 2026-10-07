import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}

new_book = {"title": "The Word for World Is Forest", "author_id": 6, "year": 1972, "price": 9.4}

r = requests.post(BASE + "/books", json=new_book, headers=AUTH)
saved = r.json()
print("status:", r.status_code)
print("location:", r.headers["Location"])
print("id:", saved["id"])
print("author:", saved["author"]["name"])
