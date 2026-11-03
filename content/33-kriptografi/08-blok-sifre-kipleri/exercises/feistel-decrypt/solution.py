import hashlib


def round_fn(key, i, half):
    return hashlib.sha256(key + bytes([i]) + half).digest()[:8]


def encrypt_block(key_hex, block_hex):
    key = bytes.fromhex(key_hex)
    block = bytes.fromhex(block_hex)
    left, right = block[:8], block[8:]
    for i in range(4):
        mixed = bytes(a ^ b for a, b in zip(left, round_fn(key, i, right)))
        left, right = right, mixed
    return (left + right).hex()


def decrypt_block(key_hex, block_hex):
    key = bytes.fromhex(key_hex)
    block = bytes.fromhex(block_hex)
    left, right = block[:8], block[8:]
    for i in reversed(range(4)):
        mixed = bytes(a ^ b for a, b in zip(right, round_fn(key, i, left)))
        left, right = mixed, left
    return (left + right).hex()


key = "746f792d626c6f636b2d6b65792d3136"
plain = b"exactly16bytes!!".hex()
cipher = encrypt_block(key, plain)
print(cipher[:16])
print(decrypt_block(key, cipher) == plain)
print(bytes.fromhex(decrypt_block(key, cipher)))
