import hashlib


def checksum(path):
    h = hashlib.sha256()
    with open(path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

print(checksum("data/notes.txt")[:16])
print(checksum("data/empty.txt")[:16])
