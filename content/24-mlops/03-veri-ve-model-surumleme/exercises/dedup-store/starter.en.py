import hashlib


def add(store, name, text):
    # Compute the hash, record the name, store the contents if missing.
    pass


store = {"objects": {}, "names": {}}
print(add(store, "v1.csv", "a,b"))
print(add(store, "v2.csv", "a,b,c"))
print(add(store, "backup.csv", "a,b"))
print("names:", len(store["names"]), "objects:", len(store["objects"]))
