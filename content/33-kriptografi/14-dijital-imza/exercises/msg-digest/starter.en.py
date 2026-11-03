import hashlib


def digest(message, n):
    return int.from_bytes(message.encode(), "big") % n

n = 104723 * 104729
print(digest("hello", n) < n)
print(digest("a" * 1000, n) == digest("a" * 999 + "b", n))
print(digest("release 2.4.1", n) == digest("release 2.4.1", n))
