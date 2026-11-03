from fnmatch import fnmatchcase


def is_allowed(policy, action):
    effects = [s["effect"] for s in policy if fnmatchcase(action, s["action"])]
    if "deny" in effects:
        return False
    return "allow" in effects

POLICY = [
    {"effect": "allow", "action": "storage:Get*"},
    {"effect": "allow", "action": "storage:List*"},
    {"effect": "deny", "action": "storage:GetSecret*"},
]
for action in ["storage:GetObject", "storage:GetSecretValue", "storage:DeleteObject"]:
    print(is_allowed(POLICY, action))
