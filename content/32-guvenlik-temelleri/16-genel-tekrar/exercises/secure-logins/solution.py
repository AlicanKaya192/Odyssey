import hashlib
import hmac

ITER = 1000


def hash_password(password, salt_hex):
    salt = bytes.fromhex(salt_hex)
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITER).hex()


def run_logins(users, attempts, max_fail):
    results = []
    fails = {}
    locked = set()
    for user, password in attempts:
        record = users.get(user)
        if record is None:
            results.append("unknown user")
            continue
        given = hash_password(password, record["salt"])
        if user in locked:
            results.append("locked")
        elif hmac.compare_digest(given, record["hash"]):
            fails[user] = 0
            results.append("ok")
        else:
            fails[user] = fails.get(user, 0) + 1
            if fails[user] >= max_fail:
                locked.add(user)
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
