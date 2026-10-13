def build_index(docs):
    return {}


def search_all(index, query):
    return []

docs = ["parcel arrived damaged", "refund for damaged item",
        "parcel is late", "app is slow"]
index = build_index(docs)
print(index["damaged"], index["parcel"])
print(search_all(index, "damaged parcel"))
print(search_all(index, "slow parcel"))
