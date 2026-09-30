import pandas as pd

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")
print(c.shape)

print(int(c["promo"].sum()), int(c["holiday"].sum()))

promo_days = c[c["promo"] == 1]
print(sorted(promo_days.index.dayofweek.unique().tolist()))

other = c[(c["promo"] == 0) & (c["holiday"] == 0)]
print(round(float(promo_days["sales"].mean()), 1),
      round(float(c.loc[c["holiday"] == 1, "sales"].mean()), 1),
      round(float(other["sales"].mean()), 1))

no_promo = c.loc[c["promo"] == 0, "sales"].mean()
print(round(float(promo_days["sales"].mean() - no_promo), 1))

print(round(float(c["sales"].corr(c["temp_c"])), 2))
