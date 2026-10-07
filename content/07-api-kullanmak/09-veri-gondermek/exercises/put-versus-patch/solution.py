import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}
CHANGE = {"title": "Changed", "price": 9.0}


def change_and_read(method, book_id):
    url = BASE + "/books/" + str(book_id)
    requests.request(method, url, json=CHANGE, headers=AUTH)
    return requests.get(url).json()


for method, book_id in [("PATCH", 15), ("PUT", 14)]:
    book = change_and_read(method, book_id)
    print(method, book["title"], book["price"], book["year"], book["tags"])
