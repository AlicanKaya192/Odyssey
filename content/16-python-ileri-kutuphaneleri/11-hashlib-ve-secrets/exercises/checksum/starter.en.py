import hashlib


def checksum(path):
    return hashlib.sha256(path.encode()).hexdigest()

print(checksum("data/notes.txt")[:16])
print(checksum("data/empty.txt")[:16])
