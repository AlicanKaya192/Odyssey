import hashlib
import hmac


def hkdf_expand(prk_hex, info_hex, length):
    prk = bytes.fromhex(prk_hex)
    info = bytes.fromhex(info_hex)
    block = hmac.new(prk, info + bytes([1]), hashlib.sha256).digest()
    return block[:length].hex()

prk = "9f" * 32
print(len(hkdf_expand(prk, b"a".hex(), 16)) // 2)
print(len(hkdf_expand(prk, b"a".hex(), 80)) // 2)
short = hkdf_expand(prk, b"a".hex(), 16)
long = hkdf_expand(prk, b"a".hex(), 80)
print(long.startswith(short))
