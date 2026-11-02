def normalize(name):
    name = name.lower()
    for old, new in [("rn", "m"), ("vv", "w"), ("0", "o"), ("1", "l")]:
        name = name.replace(old, new)
    return name


def lookalike(domain, trusted):
    if domain.lower() == trusted.lower():
        return False
    return normalize(domain) == normalize(trusted)

for name in ["examp1e.com", "example.com", "exarnple.com", "vvebsite.test", "other.com"]:
    print(name, lookalike(name, "example.com"), lookalike(name, "website.test"))
