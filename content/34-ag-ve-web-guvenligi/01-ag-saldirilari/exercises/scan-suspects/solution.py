import ipaddress


def suspects(log, limit):
    ports = {}
    for src, port in log:
        ports.setdefault(src, set()).add(port)
    found = [src for src, seen in ports.items() if len(seen) >= limit]
    return sorted(found, key=ipaddress.ip_address)

log = [["198.51.100.10", p] for p in range(20, 30)]
log += [["198.51.100.9", p] for p in [22, 80, 443]]
log += [["192.168.1.10", 443], ["192.168.1.10", 443]]
print(suspects(log, 10))
print(suspects(log, 3))
