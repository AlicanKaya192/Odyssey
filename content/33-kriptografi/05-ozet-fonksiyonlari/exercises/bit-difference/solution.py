def bit_difference(a_hex, b_hex):
    a = bytes.fromhex(a_hex)
    b = bytes.fromhex(b_hex)
    x = int.from_bytes(a, "big") ^ int.from_bytes(b, "big")
    return bin(x).count("1")

import hashlib

h1 = hashlib.sha256(b"message 1").hexdigest()
h2 = hashlib.sha256(b"message 2").hexdigest()
print(bit_difference(h1, h1))
print(0 < bit_difference(h1, h2) <= 256)
