import ipaddress


def stuffing_sources(log, limit):
    failed = {}
    for src, user, ok in log:
        if not ok:
            failed.setdefault(src, set()).add(user)
    found = [src for src, users in failed.items() if len(users) >= limit]
    return sorted(found, key=ipaddress.ip_address)

log = [["198.51.100.9", "u%d" % i, False] for i in range(12)]
log += [["198.51.100.10", "u1", False], ["192.168.1.10", "ada", True]]
print(stuffing_sources(log, 10))
print(stuffing_sources(log, 1))
