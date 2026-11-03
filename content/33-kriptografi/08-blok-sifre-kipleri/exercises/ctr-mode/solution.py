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


def ctr_crypt(key_hex, nonce_hex, data_hex):
    data = bytes.fromhex(data_hex)
    out = b""
    for n, i in enumerate(range(0, len(data), 16)):
        counter_block = nonce_hex + n.to_bytes(8, "big").hex()
        stream = bytes.fromhex(encrypt_block(key_hex, counter_block))
        out += bytes(a ^ b for a, b in zip(data[i:i + 16], stream))
    return out.hex()

key = "746f792d626c6f636b2d6b65792d3136"
nonce = "0000000000000001"
text = b"the same block!!" * 2 + b"end"
secret = ctr_crypt(key, nonce, text.hex())
print(len(secret) // 2, "bytes")
print(secret[:32] == secret[32:64])
print(bytes.fromhex(ctr_crypt(key, nonce, secret)))
