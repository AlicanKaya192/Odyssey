import ipaddress


def in_network(ip_text, cidr):
    # turn the address and network into objects, ask with in
    return False

print(in_network("192.168.1.77", "192.168.1.0/24"))
print(in_network("192.168.2.5", "192.168.1.0/24"))
print(in_network("10.20.30.40", "10.0.0.0/8"))
