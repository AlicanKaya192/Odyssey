from statsmodels.stats.power import TTestIndPower
from ab_data import make_user_log

users = make_user_log(n=8000, seed=731)
d_min = TTestIndPower().solve_power(nobs1=10000, power=0.8, alpha=0.05)
# Grup başına 10 000 kişiyle yakalanabilecek en küçük göreli etkiyi
# bought, minutes ve revenue için sırayla yazdır: ad ve f"{x:.1%}".
# Göreli MDE = d_min * sapma / ortalama.
