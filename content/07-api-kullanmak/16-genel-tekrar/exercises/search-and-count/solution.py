import requests

BASE = "http://api.odyssey.test"

params = {"tag": "scifi", "year_min": 1960, "sort": "year", "per_page": 20}
r = requests.get(BASE + "/books", params=params, timeout=10)
body = r.json()
print(r.url)
print("total:", body["meta"]["total"])
for book in body["data"]:
    print(book["year"], book["title"])
