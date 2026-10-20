import hashlib


def make_pointer(name, text):
    # Turn the text into bytes, compute the hash and the size.
    pass


pointer = make_pointer("notes.txt", "hello")
print(pointer["path"], pointer["size"])
print(pointer["sha256"][:12])
print(len(pointer["sha256"]))
print(make_pointer("copy.txt", "hello")["sha256"] == pointer["sha256"])
