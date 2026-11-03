import hashlib
import hmac


def status(record, token, now):
    # dort denetimi sirayla yap
    return "ok"

import hashlib

good = hashlib.sha256(b"tok-abc").hexdigest()
fresh = {"hash": good, "expires": 900, "used": False}
print(status(fresh, "tok-abc", 100))
print(status(fresh, "guess", 100))
print(status(fresh, "tok-abc", 900))
print(status({"hash": good, "expires": 900, "used": True}, "tok-abc", 1))
print(status(None, "tok-abc", 1))
