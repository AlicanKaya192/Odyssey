ALLOWED = {"name", "email", "bio"}


def apply_update(profile, body):
    result = dict(profile)
    for key, value in body.items():
        if key in ALLOWED:
            result[key] = value
    return result

profile = {"name": "Ada", "role": "user"}
print(apply_update(profile, {"bio": "hi", "role": "admin"}))
print(profile)
