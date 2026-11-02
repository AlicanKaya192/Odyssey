def capability_list(matrix, subject):
    caps = []
    for obj, actions in matrix[subject].items():
        for action in actions:
            caps.append(f"{obj}:{action}")
    return caps

matrix = {
    "ada": {"grades": ["write", "read"]},
    "alan": {"grades": ["read"], "payroll": ["read"]},
}
print(capability_list(matrix, "alan"))
print(capability_list(matrix, "ada"))
print(capability_list(matrix, "nobody"))
