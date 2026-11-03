DEFAULTS = {"admin", "password", "1234"}


def audit(config):
    problems = []
    # dort denetimi sirayla yap
    return problems

print(audit({"debug": True, "admin_password": "admin",
             "dir_listing": False, "https_only": False}))
print(audit({"debug": False, "admin_password": "x7#kq2",
             "dir_listing": False, "https_only": True}))
