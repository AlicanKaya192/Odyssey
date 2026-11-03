def broad_permissions(policy):
    return [s["action"] for s in policy if "*" in s["action"]]

POLICY = [
    {"effect": "allow", "action": "storage:GetObject"},
    {"effect": "allow", "action": "compute:*"},
    {"effect": "deny", "action": "*"},
    {"effect": "allow", "action": "*"},
    {"effect": "allow", "action": "compute:*"},
]
print(broad_permissions(POLICY))
