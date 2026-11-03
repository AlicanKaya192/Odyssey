import ipaddress


def suspects(log, limit):
    ports = {}
    # her kaynak icin farkli portlari bir kumede topla
    return []

log = [["198.51.100.10", p] for p in range(20, 30)]
log += [["198.51.100.9", p] for p in [22, 80, 443]]
log += [["192.168.1.10", 443], ["192.168.1.10", 443]]
print(suspects(log, 10))
print(suspects(log, 3))
