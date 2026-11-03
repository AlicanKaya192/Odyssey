import hashlib
import hmac


def make_tag(key_hex, message):
    key = bytes.fromhex(key_hex)
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()


def handle(key_hex, message, tag):
    if not hmac.compare_digest(make_tag(key_hex, message), tag):
        return "rejected"
    return "accepted: " + message

key = "5f0e2b9ac4d17733e1a6082cb94d1122"
tag = make_tag(key, "ok")
print(handle(key, "ok", tag))
print(handle(key, "tampered", tag))
print(handle(key, "ok", "00"))
