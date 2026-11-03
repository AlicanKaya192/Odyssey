import ipaddress


def zone_of(ip_text, zones):
    ip = ipaddress.ip_address(ip_text)
    best, best_len = "unknown", -1
    for name, cidr in zones:
        net = ipaddress.ip_network(cidr)
        if ip in net and net.prefixlen > best_len:
            best, best_len = name, net.prefixlen
    return best

ZONES = [["corp", "10.0.0.0/8"], ["servers", "10.20.0.0/16"],
         ["db", "10.20.5.0/24"]]
for text in ["10.20.5.9", "10.20.9.9", "10.1.1.1", "192.168.1.1"]:
    print(text, zone_of(text, ZONES))
