from statsmodels.stats.power import TTestIndPower
from ab_data import make_user_log

users = make_user_log(n=8000, seed=731)
d_min = TTestIndPower().solve_power(nobs1=10000, power=0.8, alpha=0.05)
for col in ["bought", "minutes", "revenue"]:
    mean, sd = users[col].mean(), users[col].std()
    print(col, f"{d_min * sd / mean:.1%}")
