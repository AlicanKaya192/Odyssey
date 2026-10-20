import hashlib


def add(store, name, text):
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    store["names"][name] = digest
    if digest in store["objects"]:
        return "already stored"
    store["objects"][digest] = text
    return "stored"


store = {"objects": {}, "names": {}}
print(add(store, "v1.csv", "a,b"))
print(add(store, "v2.csv", "a,b,c"))
print(add(store, "backup.csv", "a,b"))
print("names:", len(store["names"]), "objects:", len(store["objects"]))
