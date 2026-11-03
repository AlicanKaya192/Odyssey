def arp_changes(replies):
    table = {}
    changes = []
    # her cevapta eski MAC'e bak, farkliysa kaydet
    return changes

replies = [["192.168.1.1", "02:00:00:00:00:fe"],
           ["192.168.1.20", "02:00:00:00:00:14"],
           ["192.168.1.1", "02:00:00:00:00:fe"],
           ["192.168.1.1", "02:00:00:00:00:66"]]
for ip, old, new in arp_changes(replies):
    print(ip)
    print("  old", old)
    print("  new", new)
