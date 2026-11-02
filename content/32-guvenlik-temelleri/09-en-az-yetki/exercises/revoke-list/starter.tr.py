from datetime import date


def revoke_list(grants, last_used, today, max_idle):
    result = []
    # hic kullanilmayan ya da cok eskiden kullanilanlari sec
    return result

grants = [["ada", "crm:read"], ["ada", "crm:write"], ["alan", "logs:read"]]
last_used = {"ada:crm:read": "2026-10-28", "ada:crm:write": "2026-05-01"}
print(revoke_list(grants, last_used, "2026-11-02", 90))
