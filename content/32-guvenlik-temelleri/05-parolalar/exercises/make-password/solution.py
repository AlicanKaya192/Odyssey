import secrets
import string

ALPHABET = string.ascii_letters + string.digits


def make_password(length):
    while True:
        password = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if (any(c.islower() for c in password) and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)):
            return password


def classes_ok(p):
    return (any(c.islower() for c in p) and any(c.isupper() for c in p)
            and any(c.isdigit() for c in p))


passwords = [make_password(12) for _ in range(50)]
print("lengths ok:", all(len(p) == 12 for p in passwords))
print("classes ok:", all(classes_ok(p) for p in passwords))
print("unique:", len(set(passwords)))
