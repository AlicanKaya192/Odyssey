def extra_services(running, needed):
    return sorted(set(running) - set(needed))

RUNNING = ["web", "telnet", "ssh", "ftp", "telnet"]
NEEDED = ["web", "ssh", "backup"]
print(extra_services(RUNNING, NEEDED))
