import hashlib
import hmac


def hkdf_expand(prk_hex, info_hex, length):
    prk = bytes.fromhex(prk_hex)
    info = bytes.fromhex(info_hex)
    out, block, counter = b"", b"", 1
    while len(out) < length:
        step = block + info + bytes([counter])
        block = hmac.new(prk, step, hashlib.sha256).digest()
        out += block
        counter += 1
    return out[:length].hex()

prk = "9f" * 32
print(len(hkdf_expand(prk, b"a".hex(), 16)) // 2)
print(len(hkdf_expand(prk, b"a".hex(), 80)) // 2)
short = hkdf_expand(prk, b"a".hex(), 16)
long = hkdf_expand(prk, b"a".hex(), 80)
print(long.startswith(short))
