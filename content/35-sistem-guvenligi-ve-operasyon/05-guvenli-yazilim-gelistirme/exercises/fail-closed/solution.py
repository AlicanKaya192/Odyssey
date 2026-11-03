def is_admin(user, roles):
    return roles.get(user) == "admin"

ROLES = {"ada": "admin", "bob": "user"}
print(is_admin("ada", ROLES))
print(is_admin("bob", ROLES))
print(is_admin("mallory", ROLES))
