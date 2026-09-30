import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def snaive(train, h):
    last_week = train.iloc[-7:].to_numpy()
    return [last_week[i % 7] for i in range(h)]


def errors(cut):
    train = s.loc[:cut]
    test = s.loc[pd.Timestamp(cut) + pd.Timedelta(days=1):].iloc[:28]
    forecast = pd.Series(snaive(train, len(test)), index=test.index)
    return test - forecast


def evaluate(cut):
    error = errors(cut)
    return (round(float(error.abs().mean()), 2), round(float(error.mean()), 2),
            int((error > 0).sum()))


print(evaluate("2024-11-05"))
print(evaluate("2024-12-03"))

error = errors("2024-12-03")
print([round(float(error.iloc[i:i + 7].mean()), 1) for i in range(0, 28, 7)])
