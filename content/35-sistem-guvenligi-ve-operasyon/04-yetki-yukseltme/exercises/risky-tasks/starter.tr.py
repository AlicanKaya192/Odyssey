def risky_tasks(tasks):
    found = []
    for task in tasks:
        if task["mode"] & 0o002:
            found.append(task["name"])
    return found

TASKS = [
    {"name": "backup", "runs_as": "root", "owner": "root", "mode": 0o755},
    {"name": "cleanup", "runs_as": "root", "owner": "root", "mode": 0o777},
    {"name": "report", "runs_as": "root", "owner": "bob", "mode": 0o755},
    {"name": "stats", "runs_as": "bob", "owner": "bob", "mode": 0o777},
    {"name": "audit", "runs_as": "root", "owner": "root", "mode": 0o775},
]
print(risky_tasks(TASKS))
