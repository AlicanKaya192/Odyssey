import hashlib
import hmac

ITER = 1000


def hash_password(password, salt_hex):
    salt = bytes.fromhex(salt_hex)
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITER).hex()


def run_logins(users, attempts, max_fail):
    results = []
    for user, password in attempts:
        record = users[user]
        if hash_password(password, record["salt"]) == record["hash"]:
            results.append("ok")
        else:
            results.append("bad password")
    return results

users = {
    "ada": {"salt": "a1b2c3d4", "hash": hash_password("blue-river-42", "a1b2c3d4")},
    "bora": {"salt": "0f0e0d0c", "hash": hash_password("green-hill-7", "0f0e0d0c")},
}
attempts = [
    ["ada", "nope"],
    ["ada", "blue-river-42"],
    ["bora", "x"],
    ["bora", "y"],
    ["bora", "z"],
    ["bora", "green-hill-7"],
    ["zeynep", "a"],
]
for (user, _), result in zip(attempts, run_logins(users, attempts, 3)):
    print(user, result)
