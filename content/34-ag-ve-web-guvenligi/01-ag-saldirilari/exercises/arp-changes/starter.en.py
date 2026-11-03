def arp_changes(replies):
    table = {}
    changes = []
    # for each answer look at the old MAC, record it if different
    return changes

replies = [["192.168.1.1", "02:00:00:00:00:fe"],
           ["192.168.1.20", "02:00:00:00:00:14"],
           ["192.168.1.1", "02:00:00:00:00:fe"],
           ["192.168.1.1", "02:00:00:00:00:66"]]
for ip, old, new in arp_changes(replies):
    print(ip)
    print("  old", old)
    print("  new", new)
