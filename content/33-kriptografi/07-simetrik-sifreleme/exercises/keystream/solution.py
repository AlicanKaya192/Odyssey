import hashlib


def keystream(key_hex, nonce_hex, length):
    key = bytes.fromhex(key_hex)
    nonce = bytes.fromhex(nonce_hex)
    out, counter = b"", 0
    while len(out) < length:
        out += hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]

print(keystream("00" * 16, "00" * 8, 5).hex())
print(len(keystream("00" * 16, "00" * 8, 10)))
print(len(keystream("00" * 16, "00" * 8, 40)))
print(keystream("11" * 16, "22" * 8, 4).hex())
