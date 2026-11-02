from ab_data import make_experiment

test = make_experiment(n=12000, seed=741)
test["mobile"] = (test["platform"] == "mobile").astype(int)
means = test.groupby("group")[["sessions", "mobile"]].mean()
print(round(means.loc["A", "sessions"], 3), round(means.loc["B", "sessions"], 3))
print(round(means.loc["A", "mobile"], 3), round(means.loc["B", "mobile"], 3))
