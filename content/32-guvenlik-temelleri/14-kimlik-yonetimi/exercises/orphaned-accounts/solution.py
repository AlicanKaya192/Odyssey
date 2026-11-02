def orphaned_accounts(accounts, active):
    active = set(active)
    found = [f"{system}/{user}" for system, users in accounts.items()
             for user in users if user not in active]
    return sorted(found)

active = ["ada", "bora", "ceren"]
accounts = {
    "mail": ["ada", "bora", "ceren", "deniz"],
    "wiki": ["ada", "deniz"],
    "payroll": ["ceren", "emre"],
}
for item in orphaned_accounts(accounts, active):
    print(item)
