import json

record = {
    "id": 7,
    "tags": {"novel", "classic", "english"},
    "coords": (38.42, 27.14),
    "scores": {2023: 4.5, 2024: 4.8},
}

scores = {}
for year, score in record["scores"].items():
    scores[str(year)] = score

clean = {
    "id": record["id"],
    "tags": sorted(record["tags"]),
    "coords": list(record["coords"]),
    "scores": scores,
}

text = json.dumps(clean, sort_keys=True)
print(text)

back = json.loads(text)
print("same after round trip:", back == clean)
