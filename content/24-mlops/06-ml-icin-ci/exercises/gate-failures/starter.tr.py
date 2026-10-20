def gate_failures(metrics, rules):
    # Alt sinir, temel cizgiye gore pay, dilimler.
    pass


RULES = {"min_accuracy": 0.78, "min_lift": 0.05, "min_slice": 0.75}
good = {"accuracy": 0.81, "baseline": 0.70, "slices": {"pro": 0.80, "basic": 0.82}}
weak = {"accuracy": 0.70, "baseline": 0.70, "slices": {"pro": 0.65, "basic": 0.74}}
print(gate_failures(good, RULES))
for failure in gate_failures(weak, RULES):
    print(failure)
