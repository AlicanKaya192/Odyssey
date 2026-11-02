from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_experiment

test = make_experiment(n=20000, seed=742)
refund = test.groupby("group")["refunded"].agg(["sum", "count"])
print((refund["sum"] / refund["count"]).round(4).to_dict())
p = proportions_ztest(refund["sum"].to_numpy(), refund["count"].to_numpy())[1]
print(round(p, 3))
