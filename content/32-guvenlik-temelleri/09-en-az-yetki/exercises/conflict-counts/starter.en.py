def conflict_counts(user_perms, conflicts):
    counts = {}
    # count the pairs for every user
    return counts

conflicts = [["vendor:create", "payment:approve"], ["code:write", "deploy:alone"]]
user_perms = {
    "ada": ["vendor:create", "payment:approve", "code:write", "deploy:alone"],
    "alan": ["vendor:create"],
    "grace": ["code:write", "deploy:alone"],
}
print(conflict_counts(user_perms, conflicts))
