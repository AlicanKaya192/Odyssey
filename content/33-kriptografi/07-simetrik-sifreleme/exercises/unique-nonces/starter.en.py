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
    stream = keystream(key_hex, nonce_hex, len(data))
    return bytes(d ^ s for d, s in zip(data, stream)).hex()


def encrypt_all(key_hex, items):
    results = []
    for nonce_hex, data_hex in items:
        results.append(stream_encrypt(key_hex, nonce_hex, data_hex))
    return results

key = "6b6579313233343536373839306b6579"
items = [
    ["6e31", "aa"],
    ["6e32", "bb"],
    ["6e31", "cc"],
]
for result in encrypt_all(key, items):
    print(result)
