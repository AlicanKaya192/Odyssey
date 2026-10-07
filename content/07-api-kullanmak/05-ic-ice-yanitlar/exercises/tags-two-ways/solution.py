import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

items = response["data"]
for item in items:
    print(item["title"] + ":", "|".join(item["tags"]))

pairs = []
for item in items:
    for tag in item["tags"]:
        pairs.append({"book_id": item["id"], "tag": tag})

tag_counts = {}
for pair in pairs:
    tag_counts[pair["tag"]] = tag_counts.get(pair["tag"], 0) + 1

print("pairs:", len(pairs))
for tag in sorted(tag_counts):
    print(tag + ":", tag_counts[tag])
