import json

data = {
    "resultCount": 3,
    "results": [
        {"trackName": "Track One", "artistName": "Band"},
        {"trackName": "Track Two", "artistName": "Band"},
        {"trackName": "Track Three", "artistName": "Band"},
    ],
}


# İlk sonucu json.dumps(..., indent=2) ile yaz
# resultCount kadar sonucu numaralı yaz
