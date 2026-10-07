import requests

BASE = "http://api.odyssey.test"

r = requests.get(BASE + "/books", params={"author": "Orwell"})
print(r.url)

titles = []
for book in r.json()["data"]:
    titles.append(book["title"])
for title in titles:
    print(title)
