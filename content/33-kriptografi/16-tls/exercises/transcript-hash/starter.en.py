import hashlib


def transcript_hash(messages):
    h = hashlib.sha256()
    for m in sorted(messages):
        h.update(m.encode())
    return h.hexdigest()

a = transcript_hash(["client_hello", "server_hello"])
b = transcript_hash(["server_hello", "client_hello"])
print(a == b)
print(len(a))
