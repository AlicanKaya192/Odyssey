def date_status(cert, today):
    if today < cert["not_before"]:
        return "not yet valid"
    if today > cert["not_after"]:
        return "expired"
    return "ok"

cert = {"not_before": "2026-01-01", "not_after": "2026-12-31"}
print(date_status(cert, "2026-11-03"))
print(date_status(cert, "2025-12-31"))
print(date_status(cert, "2027-01-01"))
