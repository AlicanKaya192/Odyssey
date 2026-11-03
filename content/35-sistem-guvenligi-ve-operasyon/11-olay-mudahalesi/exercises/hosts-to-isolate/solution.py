def hosts_to_isolate(hosts, indicators):
    bad = set(indicators)
    return sorted(host for host, seen in hosts.items() if bad & set(seen))

HOSTS = {
    "pc-ada": ["mail.example.org", "intranet.local"],
    "pc-bob": ["update-check.example", "intranet.local"],
    "srv-db": ["203.0.113.66"],
    "srv-web": ["cdn.example.net"],
}
print(hosts_to_isolate(HOSTS, ["update-check.example", "203.0.113.66"]))
print(hosts_to_isolate(HOSTS, []))
