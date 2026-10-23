import json

data = {
    "resultCount": 3,
    "results": [
        {"trackName": "Track One", "artistName": "Band"},
        {"trackName": "Track Two", "artistName": "Band"},
        {"trackName": "Track Three", "artistName": "Band"},
    ],
}

print(json.dumps(data["results"][0], indent=2))
for i in range(data["resultCount"]):
    print(f"{i + 1}. {data['results'][i]['trackName']}")
