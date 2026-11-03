import hashlib


def digest(message, n):
    h = hashlib.sha256(message.encode()).digest()
    return int.from_bytes(h, "big") % n


def verify(message, signature, e, n):
    return pow(signature, e, n) == digest(message, n)

n = 104723 * 104729
s = 1827243129
print(verify("release 2.4.1", s, 65537, n))
print(verify("release 2.4.2", s, 65537, n))
