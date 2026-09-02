records = [
    {"name": "Ada", "city": "Ankara", "score": 82},
    {"name": "Kerem", "city": "Izmir", "score": 74},
    {"name": "Mina", "city": "Ankara", "score": 91},
    {"name": "Deniz", "city": "Izmir", "score": 68},
    {"name": "Efe", "city": "Bursa", "score": 88},
]

cities = [record["city"] for record in records]

print(cities)
print(len(set(cities)))
