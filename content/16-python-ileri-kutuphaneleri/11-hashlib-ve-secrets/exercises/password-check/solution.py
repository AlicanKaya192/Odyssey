import hashlib
import hmac


def hash_password(password, salt_hex):
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return key.hex()


def check_password(password, salt_hex, key_hex):
    return hmac.compare_digest(hash_password(password, salt_hex), key_hex)

salt = "00112233445566778899aabbccddeeff"
key = hash_password("secret123", salt)
print(key[:16], len(key))
print(check_password("secret123", salt, key), check_password("secret124", salt, key))
