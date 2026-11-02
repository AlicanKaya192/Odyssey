def xor_hex(a_hex, b_hex):
    a = bytes.fromhex(a_hex)
    b = bytes.fromhex(b_hex)
    if len(a) != len(b):
        return None
    return bytes(x ^ y for x, y in zip(a, b)).hex()

print(xor_hex("0f0f", "ffff"))
print(xor_hex("4142", "4142"))
print(xor_hex("00", "0000"))
