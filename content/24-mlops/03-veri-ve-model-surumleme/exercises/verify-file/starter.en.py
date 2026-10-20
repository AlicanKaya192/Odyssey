import hashlib


def verify(pointer, text):
    # First the size, then the hash.
    pass


pointer = {"path": "data.csv", "sha256": hashlib.sha256(b"id,plan").hexdigest(), "size": 7}
print(verify(pointer, "id,plan"))
print(verify(pointer, "id,plan,fee"))
print(verify(pointer, "id,PLAN"))
