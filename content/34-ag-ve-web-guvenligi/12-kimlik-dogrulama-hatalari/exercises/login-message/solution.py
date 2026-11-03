import hashlib
import hmac

SALT = b"lesson-salt"


def hash_pw(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SALT, 1000).hex()


DUMMY = hash_pw("dummy-password")


def login(users, user, password):
    stored = users.get(user, DUMMY)
    matches = hmac.compare_digest(stored, hash_pw(password))
    if user in users and matches:
        return "welcome"
    return "invalid user name or password"

USERS = {"ada": hash_pw("blue-river-42")}
print(login(USERS, "ada", "blue-river-42"))
print(login(USERS, "ada", "wrong"))
print(login(USERS, "zeynep", "x"))
