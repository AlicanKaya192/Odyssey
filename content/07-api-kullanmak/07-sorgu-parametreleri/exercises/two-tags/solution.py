import requests

BASE = "http://api.odyssey.test"

r = requests.get(BASE + "/books", params={"tag": ["scifi", "classic"]})
print(r.url)
for book in r.json()["data"]:
    print(book["title"])

r = requests.get(BASE + "/books", params={"tag": "scifi"})
print("scifi only:", r.json()["meta"]["total"])
