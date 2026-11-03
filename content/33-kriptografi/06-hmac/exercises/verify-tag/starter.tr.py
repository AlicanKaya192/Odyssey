import hashlib
import hmac


def make_tag(key_hex, message):
    key = bytes.fromhex(key_hex)
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()


def verify_tag(key_hex, message, tag):
    expected = make_tag(key_hex, message)
    return expected == tag

key = "5f0e2b9ac4d17733e1a6082cb94d1122"
tag = make_tag(key, "transfer 100 to bob")
print(verify_tag(key, "transfer 100 to bob", tag))
print(verify_tag(key, "transfer 900 to eve", tag))
print(verify_tag("00" * 16, "transfer 100 to bob", tag))
