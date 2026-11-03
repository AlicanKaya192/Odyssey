from ab_data import make_market

market = make_market(seed=21)
m = market.groupby("group")["completed"].mean()
print(round(float(m["B"] / m["A"] - 1), 3))
all_a = make_market(seed=21, share_b=0.0)["completed"].sum()
all_b = make_market(seed=21, share_b=1.0)["completed"].sum()
print(round(float(all_b / all_a - 1), 3))
