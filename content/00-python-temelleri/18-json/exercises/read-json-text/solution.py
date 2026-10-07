import json

text = '{"title": "Dune", "author": "Frank Herbert", "year": 1965, "available": true}'

book = json.loads(text)

print(type(book))
print(book["title"], "by", book["author"])
print(2026 - book["year"])
print(book["available"])
