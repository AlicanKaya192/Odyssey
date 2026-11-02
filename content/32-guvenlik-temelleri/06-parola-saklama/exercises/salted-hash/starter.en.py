import hashlib


def salted_hash(password, salt_hex):
    return hashlib.sha256(password.encode()).hexdigest()

salt = "8f2a1c9e5b7d3f60a4c2e8b1d6f09a37"
print(salted_hash("sunshine1", salt)[:20])
print(salted_hash("sunshine1", "00" * 16)[:20])
