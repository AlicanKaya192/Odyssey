def gap_report(required, status):
    if not required:
        return {"coverage": 100.0, "missing": [], "partial": []}
    state = {c: status.get(c, "no") for c in required}
    done = [c for c in required if state[c] == "yes"]
    missing = sorted(c for c in required if state[c] == "no")
    partial = sorted(c for c in required if state[c] == "partial")
    coverage = round(100 * len(done) / len(required), 1)
    return {"coverage": coverage, "missing": missing, "partial": partial}

required = ["access-control", "mfa", "backup", "logging", "patching"]
status = {
    "access-control": "yes",
    "mfa": "partial",
    "backup": "yes",
    "logging": "no",
}
report = gap_report(required, status)
print("coverage:", report["coverage"])
print("missing:", report["missing"])
print("partial:", report["partial"])
