import hashlib
import hmac


def hotp(secret, counter, digits=6):
    msg = counter.to_bytes(8, "big")
    digest = hmac.new(secret.encode(), msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    number = int.from_bytes(digest[offset:offset + 4], "big") & 0x7FFFFFFF
    return str(number % 10**digits).zfill(digits)


def totp(secret, unix_time, step=30, digits=6):
    return hotp(secret, unix_time // step, digits)

secret = "12345678901234567890"
for t in [59, 1111111109, 1234567890]:
    print(t, totp(secret, t))
print(totp(secret, 59, digits=8))
