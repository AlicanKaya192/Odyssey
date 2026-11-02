def effective_actions(matrix, subject, obj):
    return matrix[subject][obj]

matrix = {
    "ada": {"*": ["read"], "grades": ["write"]},
    "alan": {"payroll": ["read", "write"]},
}
print(effective_actions(matrix, "ada", "grades"))
print(effective_actions(matrix, "ada", "payroll"))
print(effective_actions(matrix, "alan", "grades"))
print(effective_actions(matrix, "mallory", "grades"))
