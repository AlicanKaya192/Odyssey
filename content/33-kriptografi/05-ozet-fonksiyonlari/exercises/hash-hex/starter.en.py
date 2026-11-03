import hashlib


def hash_hex(text, name):
    # hash with the name algorithm
    return ""

print(hash_hex("meet at noon", "sha256")[:16])
print(hash_hex("meet at noon", "sha256") == hash_hex("meet at noon", "sha256"))
print(len(hash_hex("x", "sha1")), len(hash_hex("x", "md5")))
