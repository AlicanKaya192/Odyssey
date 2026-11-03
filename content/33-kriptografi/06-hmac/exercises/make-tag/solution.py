import hashlib
import hmac


def make_tag(key_hex, message):
    key = bytes.fromhex(key_hex)
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

print(make_tag("5f0e2b9ac4d17733e1a6082cb94d1122", "transfer 100 to bob")[:16])
print(len(make_tag("5f0e2b9ac4d17733e1a6082cb94d1122", "x")))
print(make_tag("0011", "a") == make_tag("0011", "a"))
