def merge_settings(defaults, user):
    result = dict(defaults)
    for key, value in user.items():
        if key in defaults:
            result[key] = value
    return result

defaults = {"debug": False, "tls": True, "password_min": 12}
user = {"debug": True, "theme": "dark"}
result = merge_settings(defaults, user)
for key, value in result.items():
    print(key, value)
print("defaults debug:", defaults["debug"])
