import ipaddress


def zone_of(ip_text, zones):
    ip = ipaddress.ip_address(ip_text)
    for name, cidr in zones:
        if ip in ipaddress.ip_network(cidr):
            return name
    return "unknown"

ZONES = [["corp", "10.0.0.0/8"], ["servers", "10.20.0.0/16"],
         ["db", "10.20.5.0/24"]]
for text in ["10.20.5.9", "10.20.9.9", "10.1.1.1", "192.168.1.1"]:
    print(text, zone_of(text, ZONES))
