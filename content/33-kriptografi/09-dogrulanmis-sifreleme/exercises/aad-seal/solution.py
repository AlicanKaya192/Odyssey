import hashlib
import hmac


def keystream(key, nonce, length):
    out, counter = b"", 0
    while len(out) < length:
        out += hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def toy_cipher(key_hex, nonce_hex, data_hex):
    key = bytes.fromhex(key_hex)
    nonce = bytes.fromhex(nonce_hex)
    data = bytes.fromhex(data_hex)
    stream = keystream(key, nonce, len(data))
    return bytes(d ^ s for d, s in zip(data, stream)).hex()


def seal_aad(enc_key_hex, mac_key_hex, nonce_hex, header_hex, message_hex):
    cipher_hex = toy_cipher(enc_key_hex, nonce_hex, message_hex)
    mac_key = bytes.fromhex(mac_key_hex)
    header = bytes.fromhex(header_hex)
    signed = len(header).to_bytes(4, "big") + header
    signed += bytes.fromhex(nonce_hex + cipher_hex)
    tag = hmac.new(mac_key, signed, hashlib.sha256).hexdigest()
    return [cipher_hex, tag]

enc = "11" * 16
mac = "22" * 16
nonce = "00" * 8
a = seal_aad(enc, mac, nonce, b"to:ada".hex(), b"pay".hex())
b = seal_aad(enc, mac, nonce, b"to:bob".hex(), b"pay".hex())
print(a[0] == b[0])
print(a[1] == b[1])
