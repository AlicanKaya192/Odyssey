from datetime import date, timedelta


def publish_date(reported, fixed, deadline_days, grace_days):
    deadline = date.fromisoformat(reported) + timedelta(days=deadline_days)
    if fixed is None:
        return deadline.isoformat()
    after_fix = date.fromisoformat(fixed) + timedelta(days=grace_days)
    return min(deadline, after_fix).isoformat()

print(publish_date("2026-11-03", "2027-01-10", 90, 14))
print(publish_date("2026-11-03", "2027-02-20", 90, 14))
print(publish_date("2026-11-03", None, 90, 14))
