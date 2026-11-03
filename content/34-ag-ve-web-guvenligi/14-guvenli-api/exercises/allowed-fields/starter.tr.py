ALLOWED = {"name", "email", "bio"}


def apply_update(profile, body):
    result = dict(profile)
    result.update(body)
    return result

profile = {"name": "Ada", "role": "user"}
print(apply_update(profile, {"bio": "hi", "role": "admin"}))
print(profile)
