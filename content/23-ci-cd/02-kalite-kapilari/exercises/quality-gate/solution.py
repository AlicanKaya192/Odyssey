def failed_gates(results, min_coverage):
    failed = []
    if results["syntax"] != 0:
        failed.append("syntax")
    if results["format"] != 0:
        failed.append("format")
    if results["lint_errors"] > 0:
        failed.append("lint")
    if results["coverage"] < min_coverage:
        failed.append("coverage")
    return failed


def gate_message(failed):
    if len(failed) == 0:
        return "PASS"
    return "FAIL: " + ", ".join(failed)


good = {"syntax": 0, "format": 0, "lint_errors": 0, "coverage": 91}
bad = {"syntax": 0, "format": 1, "lint_errors": 3, "coverage": 72}
print(failed_gates(good, 80))
print(failed_gates(bad, 80))
print(gate_message(failed_gates(good, 80)))
print(gate_message(failed_gates(bad, 80)))
