def check_321(copies):
    failed = []
    if len(copies) < 3:
        failed.append("copies")
    # media and the copy outside
    return failed

GOOD = [
    {"media": "ssd", "offsite": False},
    {"media": "hdd", "offsite": False},
    {"media": "cloud", "offsite": True},
]
BAD = [{"media": "hdd", "offsite": False}, {"media": "hdd", "offsite": False}]
print(check_321(GOOD))
print(check_321(BAD))
