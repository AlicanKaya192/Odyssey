import pandas as pd


def parse_dates(texts):
    dates = pd.to_datetime(pd.Series(texts))
    return {"bad": 0, "dates": dates.dt.strftime("%Y-%m-%d").tolist()}

result = parse_dates(["02.03.2026", "31.02.2026", "15.03.2026", "?"])
print(result["bad"])
print(result["dates"])
