import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

# rows: id, title, price (float), author_name, author_country ("unknown")


# Her satir: "1 | Emma | 12.5 | Austen | UK"; sonda "total price: 57.44"
