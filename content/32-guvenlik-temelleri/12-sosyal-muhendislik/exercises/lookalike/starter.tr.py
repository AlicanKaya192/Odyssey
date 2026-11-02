def normalize(name):
    return name.lower()


def lookalike(domain, trusted):
    return normalize(domain) == normalize(trusted)

for name in ["examp1e.com", "example.com", "exarnple.com", "vvebsite.test", "other.com"]:
    print(name, lookalike(name, "example.com"), lookalike(name, "website.test"))
