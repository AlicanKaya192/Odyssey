import hashlib
import hmac


def make_tag(key_hex, message):
    key = bytes.fromhex(key_hex)
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()


def sign_request(key_hex, method, path, body):
    # join the three parts with newlines, sign
    canonical = method + path + body
    return make_tag(key_hex, canonical)

key = "5f0e2b9ac4d17733e1a6082cb94d1122"
print(sign_request(key, "POST", "/pay", "amount=100")[:16])
print(sign_request(key, "POST", "/pay", "amount=100") ==
      sign_request(key, "POST", "/pay", "amount=100"))
print(sign_request(key, "GET", "/pay", "amount=100") ==
      sign_request(key, "POST", "/pay", "amount=100"))
