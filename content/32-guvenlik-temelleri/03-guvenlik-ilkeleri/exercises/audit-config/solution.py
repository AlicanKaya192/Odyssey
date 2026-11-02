def audit_config(config):
    problems = []
    if config.get("debug") is True:
        problems.append("debug-on")
    if config.get("password_min", 0) < 12:
        problems.append("short-password")
    if config.get("admin_user") == "admin":
        problems.append("default-admin")
    if config.get("tls") is not True:
        problems.append("no-tls")
    return problems

config = {"debug": True, "password_min": 8, "admin_user": "admin"}
for problem in audit_config(config):
    print(problem)
print(audit_config({"tls": True, "password_min": 14}))
