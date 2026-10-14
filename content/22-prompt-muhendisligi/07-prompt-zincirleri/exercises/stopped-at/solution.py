def stopped_at(log):
    total = sum(tokens for _, _, tokens in log)
    for step, ok, _ in log:
        if not ok:
            return [step, total]
    return ["done", total]


print(stopped_at([["classify", True, 38], ["extract", False, 45]]))
print(stopped_at([["classify", True, 38], ["reply", True, 132]]))
