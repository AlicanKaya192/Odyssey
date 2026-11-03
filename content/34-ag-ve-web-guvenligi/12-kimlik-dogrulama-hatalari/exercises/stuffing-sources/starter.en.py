import ipaddress


def stuffing_sources(log, limit):
    failed = {}
    # collect the accounts each source failed on
    return []

log = [["198.51.100.9", "u%d" % i, False] for i in range(12)]
log += [["198.51.100.10", "u1", False], ["192.168.1.10", "ada", True]]
print(stuffing_sources(log, 10))
print(stuffing_sources(log, 1))
