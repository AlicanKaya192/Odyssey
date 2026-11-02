import hashlib
import hmac


def verify_password(password, record):
    parts = record.split("$")
    if len(parts) != 4 or parts[0] != "pbkdf2_sha256" or not parts[1].isdigit():
        return False
    try:
        salt = bytes.fromhex(parts[2])
    except ValueError:
        return False
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(parts[1]))
    return hmac.compare_digest(key.hex(), parts[3])

salt = "8f2a1c9e5b7d3f60a4c2e8b1d6f09a37"
key = hashlib.pbkdf2_hmac("sha256", b"sunshine1", bytes.fromhex(salt), 1000)
record = "pbkdf2_sha256$1000$" + salt + "$" + key.hex()
print(verify_password("sunshine1", record))
print(verify_password("sunshine2", record))
print(verify_password("sunshine1", "broken"))
print(verify_password("sunshine1", "md5$1$zz$00"))
