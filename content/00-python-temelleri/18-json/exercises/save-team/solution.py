import json

team = [
    {"name": "Ada", "role": "lead"},
    {"name": "Alan", "role": "dev"},
    {"name": "Grace", "role": "dev"},
]

with open("team.json", "w", encoding="utf-8") as file:
    json.dump(team, file, indent=2)

with open("team.json", encoding="utf-8") as file:
    loaded = json.load(file)

dev_count = 0
for person in loaded:
    if person["role"] == "dev":
        dev_count += 1

print(loaded == team)
print(len(loaded))
print(dev_count)
