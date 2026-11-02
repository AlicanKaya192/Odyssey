def mover_changes(old_role, new_role, roles):
    old = set(roles[old_role])
    new = set(roles[new_role])
    return {"add": sorted(new - old), "remove": sorted(old - new)}

roles = {
    "intern": ["read-wiki", "use-mail"],
    "developer": ["read-wiki", "use-mail", "push-code", "read-logs"],
    "manager": ["read-wiki", "use-mail", "approve-leave", "read-reports"],
}
change = mover_changes("developer", "manager", roles)
print("add:", change["add"])
print("remove:", change["remove"])
