import re


def error_counts(log):
    counts = {}
    # re.findall(..., log, flags=re.MULTILINE)
    return counts

LOG = """2026-03-15 10:02 ERROR disk full
2026-03-15 10:05 INFO saved
2026-03-15 10:09 ERROR timeout
2026-03-15 10:12 ERROR disk full
2026-03-15 10:13 WARNING slow"""
print(error_counts(LOG))
