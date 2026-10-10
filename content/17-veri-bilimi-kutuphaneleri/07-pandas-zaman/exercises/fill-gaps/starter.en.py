import pandas as pd


def fill_gaps(dates, values, how):
    s = pd.Series(values, index=pd.to_datetime(dates))
    return s.astype(float).tolist()

DATES = ["2026-03-02", "2026-03-03", "2026-03-06"]
for how in ["zero", "ffill", "interpolate"]:
    print(how, fill_gaps(DATES, [40, 42, 51], how))
