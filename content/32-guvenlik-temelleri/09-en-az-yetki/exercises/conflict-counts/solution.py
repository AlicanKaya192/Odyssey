def conflict_counts(user_perms, conflicts):
    counts = {}
    for user, perms in user_perms.items():
        held = set(perms)
        n = sum(1 for pair in conflicts if set(pair) <= held)
        if n:
            counts[user] = n
    return counts

conflicts = [["vendor:create", "payment:approve"], ["code:write", "deploy:alone"]]
user_perms = {
    "ada": ["vendor:create", "payment:approve", "code:write", "deploy:alone"],
    "alan": ["vendor:create"],
    "grace": ["code:write", "deploy:alone"],
}
print(conflict_counts(user_perms, conflicts))
