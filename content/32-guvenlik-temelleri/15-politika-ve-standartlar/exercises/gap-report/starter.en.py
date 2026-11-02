def gap_report(required, status):
    done = [c for c in required if status.get(c) == "yes"]
    missing = [c for c in status if status[c] == "no"]
    partial = [c for c in status if status[c] == "partial"]
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
