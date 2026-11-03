def bit_difference(a_hex, b_hex):
    a = bytes.fromhex(a_hex)
    b = bytes.fromhex(b_hex)
    # XOR the bytes, count the ones
    return 0

import hashlib

h1 = hashlib.sha256(b"message 1").hexdigest()
h2 = hashlib.sha256(b"message 2").hexdigest()
print(bit_difference(h1, h1))
print(0 < bit_difference(h1, h2) <= 256)
