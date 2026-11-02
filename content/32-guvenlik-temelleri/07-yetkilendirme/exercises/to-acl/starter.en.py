def to_acl(matrix):
    acl = {}
    # add "subject:action" for every subject and object
    return acl

matrix = {
    "ada": {"grades": ["read", "write"]},
    "alan": {"grades": ["read"], "payroll": ["read"]},
}
acl = to_acl(matrix)
for obj in sorted(acl):
    print(obj, ", ".join(acl[obj]))
