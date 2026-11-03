import ipaddress


def route(dst, tunnel_networks):
    ip = ipaddress.ip_address(dst)
    for cidr in tunnel_networks:
        if ip in ipaddress.ip_network(cidr):
            return "vpn"
    return "direct"

TUNNEL = ["10.0.0.0/8", "172.16.0.0/12"]
for dst in ["10.20.0.15", "172.20.1.1", "203.0.113.7"]:
    print(dst, route(dst, TUNNEL))
