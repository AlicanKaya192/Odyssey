from ab_data import make_novelty_test

clicks = make_novelty_test(n=10000, seed=12)
clicks["week"] = (clicks["day"] - 1) // 7 + 1
for new, part in clicks.groupby("is_new"):
    w = part.groupby(["week", "group"])["clicks"].mean().unstack()
    print(new, (w["B"] / w["A"] - 1).round(3).tolist())
