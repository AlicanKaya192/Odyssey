import hashlib
import hmac


def verify_with_password(password, salt_hex, iterations, message, tag_hex):
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen=32)
    expected = hmac.new(key, message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, tag_hex)

salt = "a1b2c3d4e5f60718293a4b5c6d7e8f90"
tag = "6be60b72f83dfc119388419552a3151fc14fe3555588686489f9103683657f64"
print(verify_with_password("sunflower", salt, 1000, "pay 100", tag))
print(verify_with_password("sunflower", salt, 1000, "pay 900", tag))
print(verify_with_password("tulip", salt, 1000, "pay 100", tag))
