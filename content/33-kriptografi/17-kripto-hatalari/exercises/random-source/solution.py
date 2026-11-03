SECRET_USES = ["token", "key", "password", "nonce", "salt"]


def random_source(purpose):
    if purpose in SECRET_USES:
        return "secrets"
    return "random"

for purpose in ["token", "dice", "salt", "simulation"]:
    print(purpose, random_source(purpose))
