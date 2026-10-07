import requests

BASE = "http://api.odyssey.test"

params = {"tag": "classic", "sort": "price", "per_page": 3}
body = requests.get(BASE + "/books", params=params).json()

for book in body["data"]:
    print(book["title"], book["price"])
print("classics in total:", body["meta"]["total"])
