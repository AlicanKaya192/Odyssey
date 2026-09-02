records = [
    {"name": "Ada", "city": "Ankara", "score": 82},
    {"name": "Kerem", "city": "Izmir", "score": 74},
    {"name": "Mina", "city": "Ankara", "score": 91},
    {"name": "Deniz", "city": "Izmir", "score": 68},
    {"name": "Efe", "city": "Bursa", "score": 88},
]

selected = [
    record
    for record in records
    if record["city"] == "Ankara" and record["score"] >= 80
]

names = [record["name"] for record in selected]

print(names)
print(len(selected))
