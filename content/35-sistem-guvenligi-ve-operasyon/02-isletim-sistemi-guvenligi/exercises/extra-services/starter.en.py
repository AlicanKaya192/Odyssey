def extra_services(running, needed):
    return [s for s in running if s not in needed]

RUNNING = ["web", "telnet", "ssh", "ftp", "telnet"]
NEEDED = ["web", "ssh", "backup"]
print(extra_services(RUNNING, NEEDED))
