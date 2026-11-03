def xor_hex(a_hex, b_hex):
    a = bytes.fromhex(a_hex)
    b = bytes.fromhex(b_hex)
    return bytes(x ^ y for x, y in zip(a, b)).hex()

print(xor_hex("0f0f", "ff00"))
print(xor_hex("68656c6c6f", "0000000000"))
print(xor_hex("aabbcc", "aa"))
