import ipaddress


def suspects(log, limit):
    ports = {}
    # collect the distinct ports of each source in a set
    return []

log = [["198.51.100.10", p] for p in range(20, 30)]
log += [["198.51.100.9", p] for p in [22, 80, 443]]
log += [["192.168.1.10", 443], ["192.168.1.10", 443]]
print(suspects(log, 10))
print(suspects(log, 3))
