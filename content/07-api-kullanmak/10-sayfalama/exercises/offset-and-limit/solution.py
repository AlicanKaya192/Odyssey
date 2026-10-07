import requests

BASE = "http://api.odyssey.test"

items = []
offset = 0
while True:
    body = requests.get(BASE + "/offset/books", params={"offset": offset, "limit": 8}).json()
    items.extend(body["items"])
    print("offset", offset, "->", len(body["items"]), "books")
    offset += body["limit"]
    if offset >= body["total"]:
        break

print("total:", len(items))
