def blocked(connections, allowed):
    result = []
    # add disallowed ports as host:port, without repeats
    return result

connections = [["192.168.1.10", 443], ["192.168.1.10", 8888],
               ["192.168.1.30", 2525], ["192.168.1.10", 8888],
               ["192.168.1.30", 53]]
for item in blocked(connections, [53, 80, 443]):
    print(item)
