def host_matches(pattern, host):
    if pattern.startswith("*."):
        suffix = pattern[1:]
        rest = host[: -len(suffix)]
        return host.endswith(suffix) and rest != "" and "." not in rest
    return pattern == host

print(host_matches("*.example.test", "shop.example.test"))
print(host_matches("*.example.test", "a.b.example.test"))
print(host_matches("shop.example.test", "shop.example.test"))
print(host_matches("*.example.test", "example.test"))
