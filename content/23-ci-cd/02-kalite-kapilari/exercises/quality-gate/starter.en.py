def failed_gates(results, min_coverage):
    # Check each gate in order; add the closed ones to the list.
    pass


def gate_message(failed):
    # An empty list is PASS; otherwise FAIL: and the joined names.
    pass


good = {"syntax": 0, "format": 0, "lint_errors": 0, "coverage": 91}
bad = {"syntax": 0, "format": 1, "lint_errors": 3, "coverage": 72}
print(failed_gates(good, 80))
print(failed_gates(bad, 80))
print(gate_message(failed_gates(good, 80)))
print(gate_message(failed_gates(bad, 80)))
