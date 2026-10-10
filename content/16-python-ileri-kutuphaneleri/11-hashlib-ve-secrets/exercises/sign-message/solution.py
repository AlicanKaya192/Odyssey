import hashlib
import hmac


def sign(key, message):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


def verify(key, message, tag):
    return hmac.compare_digest(sign(key, message), tag)

tag = sign("k1", "amount=100")
print(tag[:16])
print(verify("k1", "amount=100", tag), verify("k1", "amount=900", tag))
