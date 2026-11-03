def replies_ok(outgoing, incoming):
    started = set()
    # put the outgoing connections in the set as tuples
    return []

outgoing = [["192.168.1.10", 51514, "203.0.113.7", 443]]
incoming = [["203.0.113.7", 443, "192.168.1.10", 51514],
            ["203.0.113.7", 443, "192.168.1.10", 51999],
            ["198.51.100.9", 443, "192.168.1.10", 51514]]
print(replies_ok(outgoing, incoming))
