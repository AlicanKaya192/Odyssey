import ipaddress


def ingress_ok(src, internal):
    ip = ipaddress.ip_address(src)
    if ip.is_loopback:
        return False
    return ip not in ipaddress.ip_network(internal)

for src in ["203.0.113.7", "192.168.1.20", "127.0.0.1"]:
    print(src, ingress_ok(src, "192.168.1.0/24"))
