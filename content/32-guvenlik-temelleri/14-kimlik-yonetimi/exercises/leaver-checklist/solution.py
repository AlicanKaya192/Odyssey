def leaver_checklist(user, accounts, secrets):
    systems = sorted(s for s, users in accounts.items() if user in users)
    known = sorted(s for s, users in secrets.items() if user in users)
    return ["disable " + s for s in systems] + ["rotate " + s for s in known]

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
