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


def keys_from_password(password, salt_hex, iterations):
    salt = bytes.fromhex(salt_hex)
    master = password.encode()
    prk = hkdf_extract(salt, master)
    enc_key = hkdf_expand(prk, b"encryption", 32)
    mac_key = hkdf_expand(prk, b"mac", 32)
    return [enc_key.hex(), mac_key.hex()]

salt = "a1b2c3d4e5f60718293a4b5c6d7e8f90"
a = keys_from_password("sunflower", salt, 1000)
b = keys_from_password("sunflower", salt, 2000)
print(a[0] == a[1])
print(a[0] == b[0])
print(a == keys_from_password("sunflower", salt, 1000))
