def unknown_needs(needs):
    problems = []
    for job, waited in needs.items():
        for name in waited:
            if name not in needs:
                problems.append(job + " -> " + name)
    return problems


jobs = {
    "lint": [],
    "test": [],
    "build": ["lint", "tests"],
    "deploy": ["build", "approve"],
}
print(unknown_needs(jobs))
print(unknown_needs({"a": [], "b": ["a"]}))
