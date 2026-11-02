def orphaned_accounts(accounts, active):
    found = []
    # add every inactive account as "system/user"
    return found

active = ["ada", "bora", "ceren"]
accounts = {
    "mail": ["ada", "bora", "ceren", "deniz"],
    "wiki": ["ada", "deniz"],
    "payroll": ["ceren", "emre"],
}
for item in orphaned_accounts(accounts, active):
    print(item)
