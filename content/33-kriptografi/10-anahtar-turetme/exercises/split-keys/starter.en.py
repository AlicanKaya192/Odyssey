import hashlib
import hmac


def hkdf_extract(salt, secret):
    return hmac.new(salt, secret, hashlib.sha256).digest()


def hkdf_expand(prk, info, length):
    out, block, counter = b"", b"", 1
    while len(out) < length:
        step = block + info + bytes([counter])
        block = hmac.new(prk, step, hashlib.sha256).digest()
        out += block
        counter += 1
    return out[:length]


def derive_pair(master_hex, salt_hex):
    master = bytes.fromhex(master_hex)
    salt = bytes.fromhex(salt_hex)
    prk = hkdf_extract(salt, master)
    enc_key = hkdf_expand(prk, b"key", 32)
    mac_key = hkdf_expand(prk, b"key", 32)
    return [enc_key.hex(), mac_key.hex()]

enc, mac = derive_pair("9f" * 32, b"app-salt-v1".hex())
print(enc == mac)
print(len(enc) // 2, len(mac) // 2)
