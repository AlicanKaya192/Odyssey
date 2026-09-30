import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]

print(round(float(visits.mean()), 1), float(visits.median()), round(float(visits.std()), 1))

z = (visits - visits.mean()) / visits.std()
print(z[z.abs() > 3].index.strftime("%m-%d").tolist())


def robust(x):
    median = x.median()
    mad = (x - median).abs().median()
    return 0.6745 * (x - median) / mad


print(round(float((visits - visits.median()).abs().median()), 1))

score = robust(visits)
top = score.abs().sort_values(ascending=False).head(5)
print(top.index.strftime("%m-%d").tolist())
print([round(float(v), 1) for v in top])

day = "2024-10-08"
print(round(float(z.loc[day]), 2), round(float(score.loc[day]), 2))
