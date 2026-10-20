def check_registry(entry, disk):
    problems = []
    known = {info["version"] for info in entry["versions"]}
    for alias, version in entry["aliases"].items():
        if version not in known:
            problems.append(f"{alias}: version {version} does not exist")
    for info in entry["versions"]:
        if info["file"] not in disk:
            problems.append(f"v{info['version']}: file missing")
        elif disk[info["file"]] != info["sha256"]:
            problems.append(f"v{info['version']}: hash mismatch")
    return problems


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
