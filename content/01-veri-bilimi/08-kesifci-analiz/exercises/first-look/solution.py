import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Izmir",
             "Ankara", "Bursa", "Izmir", "Ankara", "Izmir"],
    "age": [24, 31, 28, 45, 22, 38, 52, 27, 33, 29],
    "hours": [12, 5, 9, 2, 14, 7, 3, 11, 6, 13],
    "score": [88, 62, 82, 45, 91, 70, 51, 84, 66, 89],
})

print(data.shape)
print(data.dtypes.astype(str).tolist())
print(data.isna().sum().sum())
print(data["city"].nunique())
