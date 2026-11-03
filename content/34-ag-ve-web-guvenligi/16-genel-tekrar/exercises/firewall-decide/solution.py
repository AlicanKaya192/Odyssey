import ipaddress


def decide(rules, packet):
    address = ipaddress.ip_address(packet["src"])
    for rule in rules:
        in_network = address in ipaddress.ip_network(rule["src"])
        if in_network and rule["port"] in ("*", packet["port"]):
            return rule["action"]
    return "deny"

RULES = [
    {"action": "deny", "src": "10.0.5.0/24", "port": "*"},
    {"action": "allow", "src": "10.0.0.0/8", "port": 22},
    {"action": "allow", "src": "0.0.0.0/0", "port": 443},
]
for src, port in [("10.0.5.7", 22), ("10.1.2.3", 22), ("192.168.1.5", 443), ("192.168.1.5", 22)]:
    print(src, port, decide(RULES, {"src": src, "port": port}))
