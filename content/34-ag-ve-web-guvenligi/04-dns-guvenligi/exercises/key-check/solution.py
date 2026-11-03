import hashlib
import hmac


def key_ok(presented, published):
    digest = hashlib.sha256(presented.encode()).hexdigest()
    return hmac.compare_digest(digest, published)

import hashlib

real = "example.com zone key 2026"
published = hashlib.sha256(real.encode()).hexdigest()
print(key_ok(real, published))
print(key_ok("example.com forged key", published))
