import ipaddress


def route(dst, tunnel_networks):
    # hedef tunel aglarindan birinde mi?
    return "direct"

TUNNEL = ["10.0.0.0/8", "172.16.0.0/12"]
for dst in ["10.20.0.15", "172.20.1.1", "203.0.113.7"]:
    print(dst, route(dst, TUNNEL))
