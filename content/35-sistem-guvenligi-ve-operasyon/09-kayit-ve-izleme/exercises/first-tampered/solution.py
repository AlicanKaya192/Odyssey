import hashlib


def chain(entries):
    prev = "0" * 64
    hashes = []
    for entry in entries:
        prev = hashlib.sha256((prev + entry).encode()).hexdigest()
        hashes.append(prev)
    return hashes


def first_tampered(entries, saved):
    for i, (a, b) in enumerate(zip(chain(entries), saved)):
        if a != b:
            return i
    return -1

SAVED = chain(["login ada ok", "delete report-7", "logout ada"])
print(first_tampered(["login ada ok", "delete report-7", "logout ada"], SAVED))
print(first_tampered(["login ada ok", "delete report-8", "logout ada"], SAVED))
print(first_tampered(["login eve ok", "delete report-7", "logout ada"], SAVED))
