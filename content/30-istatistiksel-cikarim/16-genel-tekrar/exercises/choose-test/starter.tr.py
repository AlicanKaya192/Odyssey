def choose_test(outcome, groups, paired, skewed):
    return "welch"


print(choose_test("mean", 2, False, False))
print(choose_test("mean", 2, True, True))
print(choose_test("rate", 3, False, False))
