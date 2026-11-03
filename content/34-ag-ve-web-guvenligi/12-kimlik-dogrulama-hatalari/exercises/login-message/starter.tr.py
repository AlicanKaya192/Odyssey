import hashlib
import hmac

SALT = b"lesson-salt"


def hash_pw(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SALT, 1000).hex()


DUMMY = hash_pw("dummy-password")


def login(users, user, password):
    if user not in users:
        return "no such user"
    if users[user] != hash_pw(password):
        return "wrong password"
    return "welcome"

USERS = {"ada": hash_pw("blue-river-42")}
print(login(USERS, "ada", "blue-river-42"))
print(login(USERS, "ada", "wrong"))
print(login(USERS, "zeynep", "x"))
