def merge_settings(defaults, user):
    result = defaults
    result.update(user)
    return result

defaults = {"debug": False, "tls": True, "password_min": 12}
user = {"debug": True, "theme": "dark"}
result = merge_settings(defaults, user)
for key, value in result.items():
    print(key, value)
print("defaults debug:", defaults["debug"])
