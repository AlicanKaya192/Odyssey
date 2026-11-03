def hosts_to_isolate(hosts, indicators):
    found = []
    # machines that saw something in common with the indicators
    return found

HOSTS = {
    "pc-ada": ["mail.example.org", "intranet.local"],
    "pc-bob": ["update-check.example", "intranet.local"],
    "srv-db": ["203.0.113.66"],
    "srv-web": ["cdn.example.net"],
}
print(hosts_to_isolate(HOSTS, ["update-check.example", "203.0.113.66"]))
print(hosts_to_isolate(HOSTS, []))
