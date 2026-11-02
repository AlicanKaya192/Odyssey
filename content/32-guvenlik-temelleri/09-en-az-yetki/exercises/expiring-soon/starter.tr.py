from datetime import date, timedelta


def expiring_soon(grants, today, days):
    result = []
    # bugun ile bugun + days arasindakileri sec
    return result

grants = [["ada", "prod-db", "2026-11-05"], ["alan", "backups", "2026-11-20"],
          ["grace", "prod-db", "2026-10-30"], ["linus", "logs", "2026-11-02"]]
print(expiring_soon(grants, "2026-11-02", 7))
