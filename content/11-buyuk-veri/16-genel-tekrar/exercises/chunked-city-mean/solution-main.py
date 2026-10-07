import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 300_000)
totals = {}
counts = {}
chunk_means = {}

for chunk in pd.read_csv("orders.csv", chunksize=70_000):
    summary = chunk.groupby("city")["unit_price"].agg(["sum", "count", "mean"])
    for city, row in summary.iterrows():
        totals[city] = totals.get(city, 0.0) + row["sum"]
        counts[city] = counts.get(city, 0) + int(row["count"])
        chunk_means.setdefault(city, []).append(row["mean"])

means = {city: totals[city] / counts[city] for city in totals}
for city in sorted(means, key=means.get, reverse=True)[:3]:
    print(city, round(means[city], 2))

wrong = sum(chunk_means["Istanbul"]) / len(chunk_means["Istanbul"])
print(round(means["Istanbul"], 4), round(wrong, 4))
