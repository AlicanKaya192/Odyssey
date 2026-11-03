from datetime import date


def late_reports(reports, today, limit):
    late = []
    for rid, received, acknowledged in reports:
        if acknowledged is None:
            continue
        days = (date.fromisoformat(acknowledged) - date.fromisoformat(received)).days
        if days > limit:
            late.append(rid)
    return sorted(late)

REPORTS = [["R-1", "2026-10-20", "2026-10-21"],
           ["R-2", "2026-10-25", None],
           ["R-3", "2026-11-01", None],
           ["R-4", "2026-10-01", "2026-10-09"]]
print(late_reports(REPORTS, "2026-11-03", 5))
