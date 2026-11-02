def is_allowed(rules, user, action):
    return action in rules.get(user, [])

rules = {"ada": ["read", "write"], "alan": ["read"]}
print(is_allowed(rules, "ada", "write"))
print(is_allowed(rules, "alan", "write"))
print(is_allowed(rules, "mallory", "read"))
