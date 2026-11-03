import ipaddress


def half_open(events):
    waiting = set()
    # add on SYN, remove on ACK
    return sorted(waiting)

events = [["SYN", "192.168.1.10"], ["SYN", "198.51.100.9"],
          ["SYN", "198.51.100.10"], ["ACK", "192.168.1.10"],
          ["SYN", "198.51.100.11"]]
for src in half_open(events):
    print(src)
