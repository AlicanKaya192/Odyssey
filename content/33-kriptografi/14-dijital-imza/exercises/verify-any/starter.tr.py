import hashlib


def digest(message, n):
    h = hashlib.sha256(message.encode()).digest()
    return int.from_bytes(h, "big") % n


def verify_any(message, signature, keys):
    e, n = keys[0]
    if pow(signature, e, n) == digest(message, n):
        return 0
    return -1

keys = [[65537, 10968372731], [65537, 10967535067]]
print(verify_any("hello", 8873282102, keys))
print(verify_any("hello", 1503027446, keys))
print(verify_any("hullo", 8873282102, keys))
