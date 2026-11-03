WELL_KNOWN = {22: "ssh", 25: "smtp", 53: "dns", 80: "http",
              443: "https", 3306: "mysql"}


def service_for(port):
    # once gecerli araligi denetle, sonra sozlukte ara
    return ""

for port in [443, 22, 8081, 70000, -1]:
    print(port, service_for(port))
