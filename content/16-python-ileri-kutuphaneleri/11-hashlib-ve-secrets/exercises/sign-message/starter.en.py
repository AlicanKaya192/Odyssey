import hashlib
import hmac


def sign(key, message):
    return hashlib.sha256(message.encode()).hexdigest()


def verify(key, message, tag):
    return sign(key, message) == tag

tag = sign("k1", "amount=100")
print(tag[:16])
print(verify("k1", "amount=100", tag), verify("k1", "amount=900", tag))
