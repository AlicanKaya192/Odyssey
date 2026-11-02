import hashlib


def pbkdf2_hex(password, salt_hex, iterations):
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return key.hex()


def make_record(password, salt_hex, iterations):
    # join the four parts with $
    return ""

record = make_record("sunshine1", "8f2a1c9e5b7d3f60a4c2e8b1d6f09a37", 1000)
for part in record.split("$"):
    print(part[:36])
