import hashlib
import hmac


def read_cookie(cookie, key):
    # split at the last dot, recompute the tag
    return None

import hashlib
import hmac

key = "server-only-secret"
tag = hmac.new(key.encode(), b"user=ada", hashlib.sha256).hexdigest()
print(read_cookie("user=ada." + tag, key))
print(read_cookie("user=eve." + tag, key))
print(read_cookie("no-dot-here", key))
