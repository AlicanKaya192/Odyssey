records = [
    {"name": "Ada", "city": "Ankara", "score": 82},
    {"name": "Kerem", "city": "Izmir", "score": 74},
    {"name": "Mina", "city": "Ankara", "score": 91},
    {"name": "Deniz", "city": "Izmir", "score": 68},
    {"name": "Efe", "city": "Bursa", "score": 88},
    {"name": "Sila", "city": "Ankara", "score": 76},
]

totals = {}
counts = {}

for record in records:
    city = record["city"]
    totals[city] = totals.get(city, 0) + record["score"]
    counts[city] = counts.get(city, 0) + 1

averages = {}
for city in totals:
    averages[city] = totals[city] / counts[city]

for city in sorted(averages):
    print(city, averages[city])
