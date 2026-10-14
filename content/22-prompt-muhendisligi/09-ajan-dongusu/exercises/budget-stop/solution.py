def budget_stop(trace, budget):
    total = 0
    for step, tokens in enumerate(trace, 1):
        total += tokens
        if total > budget:
            return [total, step]
    return [total, 0]


print(budget_stop([50, 82, 105, 128, 151], 300))
print(budget_stop([50, 82, 114], 300))
