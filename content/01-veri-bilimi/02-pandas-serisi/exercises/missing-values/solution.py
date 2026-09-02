import pandas as pd

temps = pd.Series(
    [21.0, None, 24.0, None, 27.0, 30.0],
    index=["mon", "tue", "wed", "thu", "fri", "sat"],
)

missing = temps.isna().sum()
average = temps.mean()
filled = temps.fillna(average)

print(missing)
print(temps.count(), temps.size)
print(round(average, 2))
print(filled.tolist())
