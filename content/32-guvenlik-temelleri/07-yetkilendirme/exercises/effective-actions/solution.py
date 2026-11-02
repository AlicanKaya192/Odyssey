def effective_actions(matrix, subject, obj):
    row = matrix.get(subject, {})
    actions = set(row.get(obj, [])) | set(row.get("*", []))
    return sorted(actions)

matrix = {
    "ada": {"*": ["read"], "grades": ["write"]},
    "alan": {"payroll": ["read", "write"]},
}
print(effective_actions(matrix, "ada", "grades"))
print(effective_actions(matrix, "ada", "payroll"))
print(effective_actions(matrix, "alan", "grades"))
print(effective_actions(matrix, "mallory", "grades"))
