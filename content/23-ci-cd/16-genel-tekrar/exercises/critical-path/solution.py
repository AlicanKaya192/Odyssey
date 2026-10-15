def critical_path(jobs):
    finish = {}

    def done(name):
        if name not in finish:
            minutes, needs = jobs[name]
            finish[name] = minutes + max((done(need) for need in needs), default=0)
        return finish[name]

    last = max(jobs, key=done)
    path = [last]
    while jobs[path[-1]][1]:
        path.append(max(jobs[path[-1]][1], key=done))
    return [done(last), path[::-1]]


jobs = {
    "lint": [1, []],
    "test": [4, ["lint"]],
    "docs": [2, []],
    "build": [1, ["test", "docs"]],
    "ci-ok": [0, ["lint", "test", "build", "docs"]],
}
print(critical_path(jobs))
jobs["docs"] = [7, []]
print(critical_path(jobs))
