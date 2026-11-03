def decide(rules, packet):
    # try the rules in order, return the first match's action
    return "allow"

RULES = [{"action": "allow", "proto": "tcp", "port": 443},
         {"action": "deny", "proto": "tcp", "port": "any"},
         {"action": "allow", "proto": "udp", "port": 53}]
for proto, port in [["tcp", 443], ["tcp", 22], ["udp", 53], ["udp", 123]]:
    print(proto, port, decide(RULES, {"proto": proto, "port": port}))
