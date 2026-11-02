def access_report(grants, used, conflicts):
    lines = []
    for user in sorted(grants):
        perms = set(grants[user])
        recent = set(used.get(user, []))
        for perm in sorted(perms - recent):
            lines.append(f"{user}: unused {perm}")
        for a, b in conflicts:
            if a in perms and b in perms:
                lines.append(f"{user}: conflict {a}+{b}")
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
