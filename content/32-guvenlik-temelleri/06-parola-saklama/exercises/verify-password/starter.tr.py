import hashlib
import hmac


def verify_password(password, record):
    algorithm, iterations, salt_hex, key_hex = record.split("$")
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations))
    return hmac.compare_digest(key.hex(), key_hex)

salt = "8f2a1c9e5b7d3f60a4c2e8b1d6f09a37"
key = hashlib.pbkdf2_hmac("sha256", b"sunshine1", bytes.fromhex(salt), 1000)
record = "pbkdf2_sha256$1000$" + salt + "$" + key.hex()
print(verify_password("sunshine1", record))
print(verify_password("sunshine2", record))
print(verify_password("sunshine1", "broken"))
print(verify_password("sunshine1", "md5$1$zz$00"))
