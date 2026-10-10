import hashlib
import hmac


def hash_password(password, salt_hex):
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(password, salt_hex, key_hex):
    return hash_password(password, salt_hex) == key_hex

salt = "00112233445566778899aabbccddeeff"
key = hash_password("secret123", salt)
print(key[:16], len(key))
print(check_password("secret123", salt, key), check_password("secret124", salt, key))
