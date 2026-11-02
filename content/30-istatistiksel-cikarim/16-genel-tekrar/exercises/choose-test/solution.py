def choose_test(outcome, groups, paired, skewed):
    if outcome == "rate":
        return "z-test" if groups == 2 else "chi-square"
    if groups > 2:
        return "kruskal" if skewed else "anova"
    if paired:
        return "wilcoxon" if skewed else "paired-t"
    return "mann-whitney" if skewed else "welch"


print(choose_test("mean", 2, False, False))
print(choose_test("mean", 2, True, True))
print(choose_test("rate", 3, False, False))
