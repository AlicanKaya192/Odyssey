def audit_config(config):
    problems = []
    # check the four rules in order
    return problems

config = {"debug": True, "password_min": 8, "admin_user": "admin"}
for problem in audit_config(config):
    print(problem)
print(audit_config({"tls": True, "password_min": 14}))
