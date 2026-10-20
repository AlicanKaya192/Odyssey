import hashlib


def verify(pointer, text):
    data = text.encode("utf-8")
    if len(data) != pointer["size"]:
        return "size mismatch"
    if hashlib.sha256(data).hexdigest() != pointer["sha256"]:
        return "hash mismatch"
    return "ok"


pointer = {"path": "data.csv", "sha256": hashlib.sha256(b"id,plan").hexdigest(), "size": 7}
print(verify(pointer, "id,plan"))
print(verify(pointer, "id,plan,fee"))
print(verify(pointer, "id,PLAN"))
