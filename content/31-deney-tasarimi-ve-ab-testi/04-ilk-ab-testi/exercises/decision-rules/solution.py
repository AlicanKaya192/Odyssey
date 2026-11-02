def decide(srm_p, guard_ok, low, threshold):
    if srm_p < 0.001:
        return "stop: SRM"
    if not guard_ok:
        return "stop: guardrail"
    if low >= threshold:
        return "ship"
    if low > 0:
        return "unclear"
    return "no evidence"


print(decide(0.64, True, 0.0048, 0.003))
print(decide(0.0001, True, 0.0048, 0.003))
