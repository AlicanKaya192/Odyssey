import hashlib


def keystream(key_hex, nonce_hex, length):
    key = bytes.fromhex(key_hex)
    nonce = bytes.fromhex(nonce_hex)
    out, counter = b"", 0
    while len(out) < length:
        out += hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def stream_encrypt(key_hex, nonce_hex, data_hex):
    data = bytes.fromhex(data_hex)
    # veriyle ayni uzunlukta anahtar dizisi uret, bayt bayt XOR'la
    return data.hex()

key = "6b6579313233343536373839306b6579"
nonce = "6e6f6e636531"
cipher = stream_encrypt(key, nonce, "68656c6c6f")
print(cipher != "68656c6c6f")
print(stream_encrypt(key, nonce, cipher))
