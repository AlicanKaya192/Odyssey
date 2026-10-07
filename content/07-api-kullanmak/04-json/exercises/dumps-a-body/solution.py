import json

book = {"title": "Emma", "author": "Austen", "available": True, "note": None}

text = json.dumps(book)
print(text)
print(json.dumps(book, indent=2))
