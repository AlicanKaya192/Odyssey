def safe_update(user, changes, allowed):
    result = dict(user)
    for key, value in changes.items():
        if key in allowed:
            result[key] = value
    return result

ALLOWED = ["email", "display_name"]
user = {"name": "ada", "role": "user", "email": "a@x.io"}
request = {"email": "ada@x.io", "role": "admin"}
result = safe_update(user, request, ALLOWED)
print(result["email"], result["role"])
print(user["email"], user["role"])
