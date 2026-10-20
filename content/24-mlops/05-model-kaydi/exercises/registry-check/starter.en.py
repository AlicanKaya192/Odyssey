def check_registry(entry, disk):
    # First the aliases, then the version files.
    pass


entry = {
    "versions": [
        {"version": 1, "file": "v1.pkl", "sha256": "aaa"},
        {"version": 2, "file": "v2.pkl", "sha256": "bbb"},
        {"version": 3, "file": "v3.pkl", "sha256": "ccc"},
    ],
    "aliases": {"production": 2, "staging": 4},
}
disk = {"v1.pkl": "aaa", "v2.pkl": "xxx"}
for problem in check_registry(entry, disk):
    print(problem)
