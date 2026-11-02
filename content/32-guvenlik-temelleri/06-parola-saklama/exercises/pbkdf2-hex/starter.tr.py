import hashlib


def pbkdf2_hex(password, salt_hex, iterations):
    # tek bir SHA-256 yetmez
    return hashlib.sha256(password.encode()).hexdigest()

salt = "8f2a1c9e5b7d3f60a4c2e8b1d6f09a37"
print(pbkdf2_hex("sunshine1", salt, 1000)[:24])
print(len(pbkdf2_hex("sunshine1", salt, 1000)))
