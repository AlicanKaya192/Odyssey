def reachable(links, start):
    return sorted(links.get(start, []))

links = {"laptop": ["web"], "web": ["hr-db"], "backup": ["hr-db"],
         "hr-db": []}
print(reachable(links, "laptop"))
print(reachable(links, "backup"))
print(reachable(links, "hr-db"))
