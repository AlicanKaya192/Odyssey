import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

# items: kayit listesi; ids: kimlikler


# Yazdir: "on this page: 5", "total: 23", "ids: [...]", "pages needed: N"
