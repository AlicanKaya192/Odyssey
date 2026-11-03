import hashlib


def derive_key(password, salt_hex, iterations):
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen=32)
    return key.hex()

salt = "a1b2c3d4e5f60718293a4b5c6d7e8f90"
other = "00112233445566778899aabbccddeeff"
key = derive_key("sunflower", salt, 1000)
print(len(key) // 2, "bytes")
print(key == derive_key("sunflower", salt, 1000))
print(key == derive_key("sunflower", other, 1000))
print(key == derive_key("sunflower", salt, 2000))
