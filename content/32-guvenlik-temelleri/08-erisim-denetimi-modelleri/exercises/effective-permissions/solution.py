def effective_permissions(role, role_perms, parents):
    perms = set()
    seen = set()
    todo = [role]
    while todo:
        current = todo.pop()
        if current in seen:
            continue
        seen.add(current)
        perms |= set(role_perms.get(current, []))
        todo.extend(parents.get(current, []))
    return sorted(perms)

role_perms = {"viewer": ["read"], "editor": ["write"], "admin": ["delete", "manage"]}
parents = {"admin": ["editor"], "editor": ["viewer"]}
for role in ["viewer", "editor", "admin"]:
    print(role, ", ".join(effective_permissions(role, role_perms, parents)))
