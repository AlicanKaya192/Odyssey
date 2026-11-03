def check_321(copies):
    failed = []
    if len(copies) < 3:
        failed.append("copies")
    if len({c["media"] for c in copies}) < 2:
        failed.append("media")
    if not any(c["offsite"] for c in copies):
        failed.append("offsite")
    return failed

GOOD = [
    {"media": "ssd", "offsite": False},
    {"media": "hdd", "offsite": False},
    {"media": "cloud", "offsite": True},
]
BAD = [{"media": "hdd", "offsite": False}, {"media": "hdd", "offsite": False}]
print(check_321(GOOD))
print(check_321(BAD))
