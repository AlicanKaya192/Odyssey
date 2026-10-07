import csv
import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

rows = []
for item in response["data"]:
    rows.append({
        "id": item["id"],
        "title": item["title"],
        "price": float(item["price"]),
        "author_name": item["author"]["name"],
        "tags": "|".join(item["tags"]),
    })

columns = ["id", "title", "price", "author_name", "tags"]
with open("books.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

with open("books.csv", encoding="utf-8") as handle:
    print(handle.read())
