WELL_KNOWN = {22: "ssh", 25: "smtp", 53: "dns", 80: "http",
              443: "https", 3306: "mysql"}


def service_for(port):
    if port < 0 or port > 65535:
        return "invalid"
    return WELL_KNOWN.get(port, "unknown")

for port in [443, 22, 8081, 70000, -1]:
    print(port, service_for(port))
