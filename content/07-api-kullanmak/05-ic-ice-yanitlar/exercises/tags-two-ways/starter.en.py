import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

# 1) One cell: "Emma: classic|novel"


# 2) pairs: {"book_id": ..., "tag": ...} for every book-tag pair


# 3) tag_counts, then "classic: 3" in alphabetical order
