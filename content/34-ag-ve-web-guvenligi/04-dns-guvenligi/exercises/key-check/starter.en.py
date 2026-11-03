import hashlib
import hmac


def key_ok(presented, published):
    # hash the presented key, compare
    return False

import hashlib

real = "example.com zone key 2026"
published = hashlib.sha256(real.encode()).hexdigest()
print(key_ok(real, published))
print(key_ok("example.com forged key", published))
