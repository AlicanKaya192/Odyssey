import json

with open("books.json", encoding="utf-8") as handle:
    response = json.load(handle)

# 1) Tek hucre: "Emma: classic|novel"


# 2) pairs: her kitap-etiket cifti icin {"book_id": ..., "tag": ...}


# 3) tag_counts ve abece sirasiyla "classic: 3"
