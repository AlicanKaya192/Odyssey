import hashlib
import hmac


def make_record(password, salt_hex, iterations):
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen=32)
    return f"pbkdf2_sha256${iterations}${salt_hex}${key.hex()}"


def upgrade(password, record, minimum):
    algorithm, iterations, salt_hex, key_hex = record.split("$")
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations), dklen=32)
    if not hmac.compare_digest(key.hex(), key_hex):
        return "wrong password"
    return record

salt = "a1b2c3d4e5f60718293a4b5c6d7e8f90"
old = make_record("sunflower", salt, 1000)
new = upgrade("sunflower", old, 3000)
print(new.split("$")[1])
print(upgrade("sunflower", new, 3000) == new)
print(upgrade("tulip", old, 3000))
