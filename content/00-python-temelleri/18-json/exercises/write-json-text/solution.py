import json

movie = {"title": "Arrival", "year": 2016, "genres": ["drama", "sci-fi"], "seen": False, "rating": None}

text = json.dumps(movie)
print(type(text))
print(len(text))

pretty = json.dumps(movie, indent=2)
print(pretty)
