from fnmatch import fnmatchcase


def is_allowed(policy, action):
    for statement in policy:
        if fnmatchcase(action, statement["action"]):
            return statement["effect"] == "allow"
    return False

POLICY = [
    {"effect": "allow", "action": "storage:Get*"},
    {"effect": "allow", "action": "storage:List*"},
    {"effect": "deny", "action": "storage:GetSecret*"},
]
for action in ["storage:GetObject", "storage:GetSecretValue", "storage:DeleteObject"]:
    print(is_allowed(POLICY, action))
