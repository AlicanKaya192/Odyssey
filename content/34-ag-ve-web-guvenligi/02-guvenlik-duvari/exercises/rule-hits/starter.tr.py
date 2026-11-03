def matches(rule, packet):
    return (rule["proto"] in ("any", packet["proto"])
            and rule["port"] in ("any", packet["port"]))


def rule_hits(rules, packets):
    counts = [0] * (len(rules) + 1)
    # her paket icin ilk tutan kuralin sayacini artir
    return counts

RULES = [{"action": "allow", "proto": "tcp", "port": 443},
         {"action": "allow", "proto": "tcp", "port": 22},
         {"action": "allow", "proto": "udp", "port": 53}]
packets = [{"proto": "tcp", "port": 443}, {"proto": "tcp", "port": 443},
           {"proto": "udp", "port": 53}, {"proto": "tcp", "port": 8080}]
print(rule_hits(RULES, packets))
