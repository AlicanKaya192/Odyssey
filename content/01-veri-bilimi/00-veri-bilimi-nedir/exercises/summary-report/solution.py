raw_lines = [
    "Ada,Ankara,82",
    "Kerem,Izmir,74",
    "Mina,Ankara,91",
    "Deniz,Izmir,68",
    "Efe,Bursa,88",
]

records = []
for line in raw_lines:
    parts = line.split(",")
    records.append({
        "name": parts[0],
        "city": parts[1],
        "score": int(parts[2]),
    })

scores = [record["score"] for record in records]
average = sum(scores) / len(scores)

print("Records:", len(records))
print("Lowest:", min(scores))
print("Highest:", max(scores))
print("Average:", round(average, 1))
