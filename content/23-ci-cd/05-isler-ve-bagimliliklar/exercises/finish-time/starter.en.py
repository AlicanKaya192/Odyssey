def finish_time(job, needs, minutes):
    # Find the latest of the awaited jobs, add its own duration.
    pass


needs = {"lint": [], "test": [], "build": ["lint", "test"], "deploy": ["build"]}
minutes = {"lint": 2, "test": 5, "build": 3, "deploy": 1}
for job in needs:
    print(job, finish_time(job, needs, minutes))
