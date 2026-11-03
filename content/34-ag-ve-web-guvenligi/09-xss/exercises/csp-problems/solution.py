def csp_problems(header):
    policy = {}
    for part in header.split(";"):
        words = part.split()
        if words:
            policy[words[0].lower()] = words[1:]
    sources = policy.get("script-src", policy.get("default-src"))
    if sources is None:
        return ["no-script-src"]
    problems = []
    if "'unsafe-inline'" in sources:
        problems.append("unsafe-inline")
    if "*" in sources:
        problems.append("wildcard")
    return problems

print(csp_problems("default-src 'self'"))
print(csp_problems("script-src 'self' 'unsafe-inline'"))
print(csp_problems("img-src *"))
print(csp_problems("default-src *"))
