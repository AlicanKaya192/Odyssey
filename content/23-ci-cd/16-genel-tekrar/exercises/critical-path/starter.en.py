def critical_path(jobs):
    # First write a helper that computes each job's finish minute (recursion).
    pass


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
