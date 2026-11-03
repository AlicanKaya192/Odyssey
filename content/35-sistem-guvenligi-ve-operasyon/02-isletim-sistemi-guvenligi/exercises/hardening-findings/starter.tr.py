def hardening_findings(config, rules):
    found = []
    for key, wanted, advice in rules:
        if config[key] != wanted:
            found.append(advice)
    return found

CONFIG = {"auto_update": True, "firewall": False, "guest_account": True}
RULES = [
    ["auto_update", True, "turn on updates"],
    ["firewall", True, "turn on the firewall"],
    ["guest_account", False, "disable guest"],
    ["disk_encryption", True, "encrypt the disk"],
]
for advice in hardening_findings(CONFIG, RULES):
    print(advice)
