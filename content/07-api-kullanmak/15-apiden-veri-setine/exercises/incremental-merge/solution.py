import json

import requests

BASE = "http://api.odyssey.test"

with open("last_sync.txt", encoding="utf-8") as handle:
    since = handle.read().strip()
with open("known.json", encoding="utf-8") as handle:
    known = {int(key): value for key, value in json.load(handle).items()}

changed = requests.get(BASE + "/changes", params={"since": since}, timeout=10).json()["data"]

updated = 0
added = 0
for book in changed:
    if book["id"] in known:
        updated += 1
    else:
        added += 1
    known[book["id"]] = book

print("changed:", [book["id"] for book in changed])
print("updated:", updated, "added:", added)
print("records:", len(known))
print("new last sync:", max(book["updated"] for book in changed))
