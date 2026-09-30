import pandas as pd
from statsmodels.tsa.seasonal import STL

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]


def robust(x):
    median = x.median()
    mad = (x - median).abs().median()
    return 0.6745 * (x - median) / mad


q1 = visits.quantile(0.25)
q3 = visits.quantile(0.75)
iqr = q3 - q1
flagged = visits[(visits < q1 - 1.5 * iqr) | (visits > q3 + 1.5 * iqr)]
print(len(flagged))
print(int((flagged.index > "2024-09-02").sum()))

resid = STL(visits, period=7, robust=True).fit().resid
score = robust(resid)

top = score.abs().sort_values(ascending=False).head(5)
print(top.index.strftime("%m-%d").tolist())
print([round(float(v), 1) for v in top])

print(int((score.abs() > 3.5).sum()), int((score.abs() > 20).sum()))
