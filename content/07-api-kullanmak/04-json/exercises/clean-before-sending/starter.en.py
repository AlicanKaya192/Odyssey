import json

record = {
    "id": 7,
    "tags": {"novel", "classic", "english"},
    "coords": (38.42, 27.14),
    "scores": {2023: 4.5, 2024: 4.8},
}

# clean: tags a sorted list, coords a list, scores keys as text


# text = json.dumps(clean, sort_keys=True); print it


# back = json.loads(text); print "same after round trip: ..."
