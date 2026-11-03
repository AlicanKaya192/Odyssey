import hashlib


def keystream(key_hex, nonce_hex, length):
    key = bytes.fromhex(key_hex)
    nonce = bytes.fromhex(nonce_hex)
    block = hashlib.sha256(key + nonce).digest()
    return block[:length]

print(keystream("00" * 16, "00" * 8, 5).hex())
print(len(keystream("00" * 16, "00" * 8, 10)))
print(len(keystream("00" * 16, "00" * 8, 40)))
print(keystream("11" * 16, "22" * 8, 4).hex())
