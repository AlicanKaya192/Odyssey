import hashlib
import hmac


def hotp(secret, counter, digits=6):
    msg = counter.to_bytes(8, "big")
    # HMAC-SHA1, dynamic truncation, last digits
    return ""

secret = "12345678901234567890"
for counter in range(4):
    print(counter, hotp(secret, counter))
print(hotp(secret, 1, 8))
