def broad_permissions(policy):
    found = set()
    for s in policy:
        action = s["action"]
        if s["effect"] == "allow" and (action == "*" or action.endswith(":*")):
            found.add(action)
    return sorted(found)

POLICY = [
    {"effect": "allow", "action": "storage:GetObject"},
    {"effect": "allow", "action": "compute:*"},
    {"effect": "deny", "action": "*"},
    {"effect": "allow", "action": "*"},
    {"effect": "allow", "action": "compute:*"},
]
print(broad_permissions(POLICY))
