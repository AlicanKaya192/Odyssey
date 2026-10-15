def critical_path(jobs):
    # Once her isin bitis dakikasini hesaplayan bir yardimci yaz (ozyineleme).
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
