import hashlib
import hmac


def derive(shared):
    return hmac.new(b"session", shared.to_bytes(8, "big"), hashlib.sha256).hexdigest()


def session_key(p, g, a, b):
    ada_public = pow(g, a, p)
    can_public = pow(g, b, p)
    ada_key = derive(pow(ada_public, a, p))
    can_key = derive(pow(ada_public, b, p))
    return [ada_key == can_key, ada_key]

same, key = session_key(4294967291, 5, 1234567, 7654321)
print(same)
print(len(key) // 2, "bytes")
