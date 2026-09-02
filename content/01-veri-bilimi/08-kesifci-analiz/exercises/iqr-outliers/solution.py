import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Izmir",
             "Ankara", "Bursa", "Izmir", "Ankara", "Izmir"],
    "age": [24, 31, 28, 45, 22, 38, 52, 27, 33, 29],
    "hours": [12, 5, 9, 2, 14, 7, 3, 11, 6, 13],
    "score": [88, 62, 82, 45, 91, 70, 51, 84, 66, 89],
})

values = pd.Series([48, 52, 50, 51, 49, 53, 50, 140])

q1 = values.quantile(0.25)
q3 = values.quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

print(q1, q3)
print(low, high)
print(values[(values < low) | (values > high)].tolist())
print(round(values.mean(), 2), values.median())
