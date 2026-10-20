import hashlib


def add(store, name, text):
    # Ozeti hesapla, adi kaydet, icerik yoksa sakla.
    pass


store = {"objects": {}, "names": {}}
print(add(store, "v1.csv", "a,b"))
print(add(store, "v2.csv", "a,b,c"))
print(add(store, "backup.csv", "a,b"))
print("names:", len(store["names"]), "objects:", len(store["objects"]))
