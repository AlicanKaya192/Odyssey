def to_acl(matrix):
    acl = {}
    for subject, row in matrix.items():
        for obj, actions in row.items():
            for action in actions:
                acl.setdefault(obj, []).append(f"{subject}:{action}")
    return {obj: sorted(entries) for obj, entries in acl.items()}

matrix = {
    "ada": {"grades": ["read", "write"]},
    "alan": {"grades": ["read"], "payroll": ["read"]},
}
acl = to_acl(matrix)
for obj in sorted(acl):
    print(obj, ", ".join(acl[obj]))
