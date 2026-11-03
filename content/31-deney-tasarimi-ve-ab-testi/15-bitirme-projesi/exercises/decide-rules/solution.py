def decide(srm_p, guard_high, low, high, threshold=0.003, guard_limit=2.0):
    if srm_p < 0.001:
        return "stop: SRM"
    if guard_high >= guard_limit:
        return "stop: guardrail"
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"


print(decide(0.33, 0.99, 0.0086, 0.0207))
print(decide(0.0001, 0.5, 0.0086, 0.0207))
