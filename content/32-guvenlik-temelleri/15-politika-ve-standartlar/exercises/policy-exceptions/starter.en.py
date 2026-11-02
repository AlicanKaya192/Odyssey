def policy_exceptions(exceptions, today):
    problems = []
    for e in exceptions:
        if e["expires"] < today:
            problems.append(e["id"] + ": expired")
    return problems

exceptions = [
    {"id": "EX-3", "owner": "ceren", "expires": "2026-04-30",
     "compensating": "separate network"},
    {"id": "EX-1", "owner": "", "expires": "2026-09-01", "compensating": ""},
    {"id": "EX-2", "owner": "bora", "expires": "2026-05-01",
     "compensating": "access logged"},
    {"id": "EX-4", "owner": "ada", "compensating": "manual review"},
]
for problem in policy_exceptions(exceptions, "2026-05-01"):
    print(problem)
