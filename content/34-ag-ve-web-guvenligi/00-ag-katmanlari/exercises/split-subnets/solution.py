import ipaddress


def split(cidr, new_prefix):
    net = ipaddress.ip_network(cidr)
    return [str(part) for part in net.subnets(new_prefix=new_prefix)]

for part in split("192.168.1.0/24", 26):
    print(part)
print(len(split("10.0.0.0/16", 24)))
