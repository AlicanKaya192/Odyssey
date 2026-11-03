from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment

test = make_experiment(n=12000, seed=46, lift=0.1)
k = test.groupby("group")["bought"].sum()
n = test.groupby("group").size()
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
rate_a, rate_b = k["A"] / n["A"], k["B"] / n["B"]
diff = (rate_b - rate_a) * 100
print(f"A {rate_a:.2%} -> B {rate_b:.2%}: {diff:+.2f} pts")
print(f"95% CI {low * 100:.2f} to {high * 100:.2f}")
print(f"relative {rate_b / rate_a - 1:+.1%}")
