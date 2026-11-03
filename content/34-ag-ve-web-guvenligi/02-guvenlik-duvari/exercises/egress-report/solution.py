def blocked(connections, allowed):
    result = []
    for host, port in connections:
        item = f"{host}:{port}"
        if port not in allowed and item not in result:
            result.append(item)
    return result

connections = [["192.168.1.10", 443], ["192.168.1.10", 8888],
               ["192.168.1.30", 2525], ["192.168.1.10", 8888],
               ["192.168.1.30", 53]]
for item in blocked(connections, [53, 80, 443]):
    print(item)
