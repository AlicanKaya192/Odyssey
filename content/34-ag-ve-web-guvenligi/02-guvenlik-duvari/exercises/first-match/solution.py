def decide(rules, packet):
    for rule in rules:
        if (rule["proto"] in ("any", packet["proto"])
                and rule["port"] in ("any", packet["port"])):
            return rule["action"]
    return "deny"

RULES = [{"action": "allow", "proto": "tcp", "port": 443},
         {"action": "deny", "proto": "tcp", "port": "any"},
         {"action": "allow", "proto": "udp", "port": 53}]
for proto, port in [["tcp", 443], ["tcp", 22], ["udp", 53], ["udp", 123]]:
    print(proto, port, decide(RULES, {"proto": proto, "port": port}))
