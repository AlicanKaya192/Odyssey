import hashlib


def digest(message, n):
    h = hashlib.sha256(message.encode()).digest()
    return int.from_bytes(h, "big") % n


def sign(message, d, n):
    h = digest(message, n)
    return pow(h, 65537, n)

n = 104723 * 104729
d = 10195862609
s = sign("release 2.4.1", d, n)
print(pow(s, 65537, n) == digest("release 2.4.1", n))
