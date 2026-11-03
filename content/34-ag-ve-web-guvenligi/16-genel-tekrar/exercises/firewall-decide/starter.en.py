import ipaddress


def decide(rules, packet):
    decision = "allow"
    for rule in rules:
        if packet["src"] == rule["src"] and rule["port"] in ("*", packet["port"]):
            decision = rule["action"]
    return decision

RULES = [
    {"action": "deny", "src": "10.0.5.0/24", "port": "*"},
    {"action": "allow", "src": "10.0.0.0/8", "port": 22},
    {"action": "allow", "src": "0.0.0.0/0", "port": 443},
]
for src, port in [("10.0.5.7", 22), ("10.1.2.3", 22), ("192.168.1.5", 443), ("192.168.1.5", 22)]:
    print(src, port, decide(RULES, {"src": src, "port": port}))
