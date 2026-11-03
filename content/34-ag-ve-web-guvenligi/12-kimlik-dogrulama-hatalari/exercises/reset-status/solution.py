import hashlib
import hmac


def status(record, token, now):
    if record is None:
        return "invalid"
    if record["used"]:
        return "used"
    if now >= record["expires"]:
        return "expired"
    digest = hashlib.sha256(token.encode()).hexdigest()
    if not hmac.compare_digest(record["hash"], digest):
        return "invalid"
    return "ok"

import hashlib

good = hashlib.sha256(b"tok-abc").hexdigest()
fresh = {"hash": good, "expires": 900, "used": False}
print(status(fresh, "tok-abc", 100))
print(status(fresh, "guess", 100))
print(status(fresh, "tok-abc", 900))
print(status({"hash": good, "expires": 900, "used": True}, "tok-abc", 1))
print(status(None, "tok-abc", 1))
