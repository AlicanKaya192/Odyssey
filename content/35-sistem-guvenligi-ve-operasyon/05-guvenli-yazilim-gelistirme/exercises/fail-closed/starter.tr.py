def is_admin(user, roles):
    try:
        return roles[user] == "admin"
    except Exception:
        return True

ROLES = {"ada": "admin", "bob": "user"}
print(is_admin("ada", ROLES))
print(is_admin("bob", ROLES))
print(is_admin("mallory", ROLES))
