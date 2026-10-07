import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

rows = []
for item in response["data"]:
    author = item["author"]
    rows.append({
        "id": item["id"],
        "title": item["title"],
        "price": float(item["price"]),
        "author_name": author["name"],
        "author_country": author.get("country", "unknown"),
    })

total = 0
for row in rows:
    print(row["id"], "|", row["title"], "|", row["price"], "|", row["author_name"], "|", row["author_country"])
    total += row["price"]
print(f"total price: {total:.2f}")
