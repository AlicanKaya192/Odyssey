def access_report(grants, used, conflicts):
    lines = []
    for user, perms in grants.items():
        for perm in perms:
            if perm not in used[user]:
                lines.append(f"{user}: unused {perm}")
    return lines

grants = {
    "ada": ["pay-create", "pay-approve", "read-reports"],
    "bora": ["read-reports"],
    "ceren": ["user-create", "read-logs"],
}
used = {"ada": ["pay-create", "pay-approve"], "ceren": ["user-create"]}
conflicts = [
    ["pay-create", "pay-approve"],
    ["user-create", "user-approve"],
]
for line in access_report(grants, used, conflicts):
    print(line)
