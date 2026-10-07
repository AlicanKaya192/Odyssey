import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

items = response["data"]
ids = []
for item in items:
    ids.append(item["id"])

total = response["meta"]["total"]
per_page = response["meta"]["per_page"]
print("on this page:", len(items))
print("total:", total)
print("ids:", ids)
print("pages needed:", (total + per_page - 1) // per_page)
