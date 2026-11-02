from datetime import date


def revoke_list(grants, last_used, today, max_idle):
    now = date.fromisoformat(today)
    result = []
    for user, perm in grants:
        key = f"{user}:{perm}"
        if key not in last_used:
            result.append(key)
        elif (now - date.fromisoformat(last_used[key])).days > max_idle:
            result.append(key)
    return sorted(result)

grants = [["ada", "crm:read"], ["ada", "crm:write"], ["alan", "logs:read"]]
last_used = {"ada:crm:read": "2026-10-28", "ada:crm:write": "2026-05-01"}
print(revoke_list(grants, last_used, "2026-11-02", 90))
