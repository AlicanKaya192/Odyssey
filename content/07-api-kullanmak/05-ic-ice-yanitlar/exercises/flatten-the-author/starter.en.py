import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

# rows: id, title, price (float), author_name, author_country ("unknown")


# Each row: "1 | Emma | 12.5 | Austen | UK"; at the end "total price: 57.44"
