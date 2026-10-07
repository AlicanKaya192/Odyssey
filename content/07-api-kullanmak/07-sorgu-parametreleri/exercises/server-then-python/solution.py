import requests

BASE = "http://api.odyssey.test"

books = requests.get(BASE + "/books", params={"tag": "classic", "per_page": 20}).json()["data"]

cheap = [book for book in books if book["price"] < 10]
cheap.sort(key=lambda book: book["price"])

for book in cheap:
    print(book["title"], book["price"])
print("cheap classics:", len(cheap))
