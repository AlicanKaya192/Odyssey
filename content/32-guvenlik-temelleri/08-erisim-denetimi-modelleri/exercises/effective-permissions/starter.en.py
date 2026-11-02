def effective_permissions(role, role_perms, parents):
    perms = set(role_perms.get(role, []))
    for parent in parents.get(role, []):
        perms |= set(role_perms.get(parent, []))
    return sorted(perms)

role_perms = {"viewer": ["read"], "editor": ["write"], "admin": ["delete", "manage"]}
parents = {"admin": ["editor"], "editor": ["viewer"]}
for role in ["viewer", "editor", "admin"]:
    print(role, ", ".join(effective_permissions(role, role_perms, parents)))
