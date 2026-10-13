def build_index(docs):
    index = {}
    for i, doc in enumerate(docs):
        for word in set(doc.lower().split()):
            index.setdefault(word, []).append(i)
    return index


def search_all(index, query):
    sets = [set(index.get(w, [])) for w in query.lower().split()]
    if not sets:
        return []
    return sorted(set.intersection(*sets))

docs = ["parcel arrived damaged", "refund for damaged item",
        "parcel is late", "app is slow"]
index = build_index(docs)
print(index["damaged"], index["parcel"])
print(search_all(index, "damaged parcel"))
print(search_all(index, "slow parcel"))
