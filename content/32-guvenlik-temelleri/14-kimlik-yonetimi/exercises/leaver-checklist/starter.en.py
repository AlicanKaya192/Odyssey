def leaver_checklist(user, accounts, secrets):
    tasks = []
    for system, users in accounts.items():
        if user in users:
            tasks.append("disable " + system)
    return tasks

accounts = {
    "mail": ["ada", "deniz"],
    "wiki": ["deniz"],
    "payroll": ["ceren"],
}
secrets = {
    "shared-printer": ["ada", "deniz"],
    "deploy-key": ["deniz"],
    "wifi-guest": ["bora"],
}
for task in leaver_checklist("deniz", accounts, secrets):
    print(task)
print(leaver_checklist("emre", accounts, secrets))
