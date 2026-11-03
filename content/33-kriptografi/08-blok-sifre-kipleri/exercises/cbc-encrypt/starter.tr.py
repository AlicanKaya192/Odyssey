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


def cbc_encrypt(key_hex, iv_hex, data_hex):
    data = bytes.fromhex(data_hex)
    prev = bytes.fromhex(iv_hex)
    out = b""
    for i in range(0, len(data), 16):
        block = bytes(a ^ b for a, b in zip(data[i:i + 16], prev))
        cipher = bytes.fromhex(encrypt_block(key_hex, block.hex()))
        out += cipher
    return out.hex()

key = "746f792d626c6f636b2d6b65792d3136"
iv = "000102030405060708090a0b0c0d0e0f"
same = "59454c4c4f57205355424d4152494e45" * 2
cipher = cbc_encrypt(key, iv, same)
print(cipher[:32] == cipher[32:])
print(len(cipher) // 2, "bytes")
