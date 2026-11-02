import hashlib
import hmac


def hotp(secret, counter, digits=6):
    msg = counter.to_bytes(8, "big")
    digest = hmac.new(secret.encode(), msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    number = int.from_bytes(digest[offset:offset + 4], "big") & 0x7FFFFFFF
    return str(number % 10**digits).zfill(digits)


def verify_code(secret, code, unix_time):
    counter = unix_time // 30
    for step in (counter - 1, counter, counter + 1):
        if hmac.compare_digest(code, hotp(secret, step)):
            return True
    return False

secret = "12345678901234567890"
now = 1111111109
code = hotp(secret, now // 30)
old = hotp(secret, now // 30 - 1)
older = hotp(secret, now // 30 - 2)
print(verify_code(secret, code, now))
print(verify_code(secret, old, now))
print(verify_code(secret, older, now))
print(verify_code(secret, "000000", now))
