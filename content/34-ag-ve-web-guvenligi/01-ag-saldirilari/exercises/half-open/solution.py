import ipaddress


def half_open(events):
    waiting = set()
    for kind, src in events:
        if kind == "SYN":
            waiting.add(src)
        elif kind == "ACK":
            waiting.discard(src)
    return sorted(waiting, key=ipaddress.ip_address)

events = [["SYN", "192.168.1.10"], ["SYN", "198.51.100.9"],
          ["SYN", "198.51.100.10"], ["ACK", "192.168.1.10"],
          ["SYN", "198.51.100.11"]]
for src in half_open(events):
    print(src)
