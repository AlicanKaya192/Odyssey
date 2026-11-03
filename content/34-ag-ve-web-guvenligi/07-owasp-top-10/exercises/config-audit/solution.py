DEFAULTS = {"admin", "password", "1234"}


def audit(config):
    problems = []
    if config["debug"]:
        problems.append("debug")
    if config["admin_password"] in DEFAULTS:
        problems.append("default-password")
    if config["dir_listing"]:
        problems.append("listing")
    if not config["https_only"]:
        problems.append("http")
    return problems

print(audit({"debug": True, "admin_password": "admin",
             "dir_listing": False, "https_only": False}))
print(audit({"debug": False, "admin_password": "x7#kq2",
             "dir_listing": False, "https_only": True}))
