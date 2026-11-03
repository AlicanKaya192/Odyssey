import hashlib
import hmac


def sign(secret, ts, body):
    message = f"{ts}\n{body}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


def verify(secret, ts, now, body, signature):
    if abs(now - ts) > 300:
        return "expired"
    expected = sign(secret, ts, body)
    if not hmac.compare_digest(expected, signature):
        return "bad signature"
    return "ok"

sig = sign("demo", 1000, '{"amount": 10}')
print(verify("demo", 1000, 1030, '{"amount": 10}', sig))
print(verify("demo", 1000, 1030, '{"amount": 99}', sig))
print(verify("demo", 1000, 1400, '{"amount": 10}', sig))
