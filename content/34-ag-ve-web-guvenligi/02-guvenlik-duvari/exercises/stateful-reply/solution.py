def replies_ok(outgoing, incoming):
    started = {tuple(c) for c in outgoing}
    result = []
    for src, sport, dst, dport in incoming:
        result.append((dst, dport, src, sport) in started)
    return result

outgoing = [["192.168.1.10", 51514, "203.0.113.7", 443]]
incoming = [["203.0.113.7", 443, "192.168.1.10", 51514],
            ["203.0.113.7", 443, "192.168.1.10", 51999],
            ["198.51.100.9", 443, "192.168.1.10", 51514]]
print(replies_ok(outgoing, incoming))
