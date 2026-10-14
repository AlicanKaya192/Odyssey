def failed_gates(results, min_coverage):
    # Her kapiyi sirayla denetle; kapananlari listeye ekle.
    pass


def gate_message(failed):
    # Bos liste PASS; degilse FAIL: ile birlesik adlar.
    pass


good = {"syntax": 0, "format": 0, "lint_errors": 0, "coverage": 91}
bad = {"syntax": 0, "format": 1, "lint_errors": 3, "coverage": 72}
print(failed_gates(good, 80))
print(failed_gates(bad, 80))
print(gate_message(failed_gates(good, 80)))
print(gate_message(failed_gates(bad, 80)))
