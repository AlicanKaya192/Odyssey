def stopped_at(log):
    return ["done", 0]


print(stopped_at([["classify", True, 38], ["extract", False, 45]]))
print(stopped_at([["classify", True, 38], ["reply", True, 132]]))
