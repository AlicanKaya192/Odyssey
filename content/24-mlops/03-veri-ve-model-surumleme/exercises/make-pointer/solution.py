import hashlib


def make_pointer(name, text):
    data = text.encode("utf-8")
    return {"path": name, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


pointer = make_pointer("notes.txt", "hello")
print(pointer["path"], pointer["size"])
print(pointer["sha256"][:12])
print(len(pointer["sha256"]))
print(make_pointer("copy.txt", "hello")["sha256"] == pointer["sha256"])
