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


def seal(enc_key_hex, mac_key_hex, nonce_hex, message_hex):
    cipher_hex = toy_cipher(enc_key_hex, nonce_hex, message_hex)
    mac_key = bytes.fromhex(mac_key_hex)
    signed = bytes.fromhex(nonce_hex + cipher_hex)
    tag = hmac.new(mac_key, signed, hashlib.sha256).hexdigest()
    return nonce_hex + cipher_hex + tag


def open_box(enc_key_hex, mac_key_hex, box_hex):
    nonce_hex = box_hex[:16]
    cipher_hex = box_hex[16:-64]
    tag_hex = box_hex[-64:]
    return toy_cipher(enc_key_hex, nonce_hex, cipher_hex)

enc = "11" * 16
mac = "22" * 16
box = seal(enc, mac, "00" * 8, b"pay 100".hex())
print(bytes.fromhex(open_box(enc, mac, box)))
changed = box[:16] + "ff" + box[18:]
print(open_box(enc, mac, changed))
print(open_box(enc, "33" * 16, box))
