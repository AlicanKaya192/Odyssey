def audit_codes(release, min_gain):
    # One if per rule; add the codes in order.
    pass


release = {"seed": None, "data_digest": "", "trained_month": 5,
           "gate_month": 0, "gain": 0.001, "threshold": 0.5,
           "fallback": None, "monitors": ["accuracy"]}
for code in audit_codes(release, 0.003):
    print(code)
good = {"seed": 7, "data_digest": "2448b83141ea", "trained_month": 5,
        "gate_month": 5, "gain": 0.01, "threshold": 0.31,
        "fallback": "rule", "monitors": ["drift", "calibration"]}
print(audit_codes(good, 0.003))
