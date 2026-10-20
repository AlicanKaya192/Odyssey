def gate_failures(metrics, rules):
    failures = []
    if metrics["accuracy"] < rules["min_accuracy"]:
        failures.append("accuracy")
    if metrics["accuracy"] < metrics["baseline"] + rules["min_lift"]:
        failures.append("lift")
    for name in sorted(metrics["slices"]):
        if metrics["slices"][name] < rules["min_slice"]:
            failures.append("slice:" + name)
    return failures


RULES = {"min_accuracy": 0.78, "min_lift": 0.05, "min_slice": 0.75}
good = {"accuracy": 0.81, "baseline": 0.70, "slices": {"pro": 0.80, "basic": 0.82}}
weak = {"accuracy": 0.70, "baseline": 0.70, "slices": {"pro": 0.65, "basic": 0.74}}
print(gate_failures(good, RULES))
for failure in gate_failures(weak, RULES):
    print(failure)
