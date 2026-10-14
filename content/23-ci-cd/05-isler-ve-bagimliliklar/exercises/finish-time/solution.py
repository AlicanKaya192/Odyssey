def finish_time(job, needs, minutes):
    start = 0
    for name in needs[job]:
        start = max(start, finish_time(name, needs, minutes))
    return start + minutes[job]


needs = {"lint": [], "test": [], "build": ["lint", "test"], "deploy": ["build"]}
minutes = {"lint": 2, "test": 5, "build": 3, "deploy": 1}
for job in needs:
    print(job, finish_time(job, needs, minutes))
