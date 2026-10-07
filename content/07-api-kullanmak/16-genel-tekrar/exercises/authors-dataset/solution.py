import csv

import requests

BASE = "http://api.odyssey.test"

rows = []
for author in requests.get(BASE + "/authors", timeout=10).json()["data"]:
    books = requests.get(BASE + "/authors/" + str(author["id"]) + "/books", timeout=10).json()["data"]
    years = [book["year"] for book in books]
    prices = [book["price"] for book in books]
    rows.append({
        "name": author["name"],
        "country": author["country"],
        "books": len(books),
        "first": min(years),
        "last": max(years),
        "avg_price": round(sum(prices) / len(prices), 2),
    })

with open("authors.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

with open("authors.csv", encoding="utf-8") as handle:
    print(handle.read().strip())
