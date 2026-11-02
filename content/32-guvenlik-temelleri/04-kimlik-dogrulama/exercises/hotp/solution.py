import hashlib
import hmac


def hotp(secret, counter, digits=6):
    msg = counter.to_bytes(8, "big")
    digest = hmac.new(secret.encode(), msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    number = int.from_bytes(digest[offset:offset + 4], "big") & 0x7FFFFFFF
    return str(number % 10**digits).zfill(digits)

secret = "12345678901234567890"
for counter in range(4):
    print(counter, hotp(secret, counter))
print(hotp(secret, 1, 8))
