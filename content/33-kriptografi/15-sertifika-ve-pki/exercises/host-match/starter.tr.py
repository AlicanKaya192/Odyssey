def host_matches(pattern, host):
    if pattern.startswith("*."):
        return host.endswith(pattern[1:])
    return pattern == host

print(host_matches("*.example.test", "shop.example.test"))
print(host_matches("*.example.test", "a.b.example.test"))
print(host_matches("shop.example.test", "shop.example.test"))
print(host_matches("*.example.test", "example.test"))
