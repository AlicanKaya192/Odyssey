import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

# items: the list of records; ids: the identifiers


# Print: "on this page: 5", "total: 23", "ids: [...]", "pages needed: N"
