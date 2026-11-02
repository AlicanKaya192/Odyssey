def can_access(user, action, doc, user_roles, role_perms):
    for role in user_roles.get(user, []):
        if action in role_perms.get(role, []):
            return True
    return doc["owner"] == user and action in ("read", "edit")

user_roles = {"ada": ["editor"], "bora": ["viewer"], "ceren": []}
role_perms = {
    "viewer": ["read"],
    "editor": ["read", "edit"],
    "admin": ["read", "edit", "delete"],
}
doc = {"id": "d1", "owner": "ceren"}
checks = [
    ["ada", "edit"],
    ["bora", "edit"],
    ["ceren", "edit"],
    ["ceren", "delete"],
    ["zeynep", "read"],
]
for user, action in checks:
    print(user, action, can_access(user, action, doc, user_roles, role_perms))
