def explain_access(user, permission, user_roles, role_perms):
    reasons = []
    # kullanicinin her rolune bak
    return reasons

user_roles = {"ada": ["teacher", "admin"], "alan": ["student"]}
role_perms = {"teacher": ["grades:read", "grades:write"], "admin": ["grades:read", "users:manage"],
              "student": ["grades:read_own"]}
print(explain_access("ada", "grades:read", user_roles, role_perms))
print(explain_access("alan", "grades:write", user_roles, role_perms))
