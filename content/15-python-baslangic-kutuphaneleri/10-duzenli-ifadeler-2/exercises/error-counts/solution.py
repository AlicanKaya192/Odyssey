import re

ERROR_LINE = re.compile(r"^\S+ \S+ ERROR (.+)$", re.MULTILINE)


def error_counts(log):
    counts = {}
    for message in ERROR_LINE.findall(log):
        counts[message] = counts.get(message, 0) + 1
    return counts

LOG = """2026-03-15 10:02 ERROR disk full
2026-03-15 10:05 INFO saved
2026-03-15 10:09 ERROR timeout
2026-03-15 10:12 ERROR disk full
2026-03-15 10:13 WARNING slow"""
print(error_counts(LOG))
