import dask.dataframe as dd
from orders_data import make_orders

orders = make_orders(120_000)

orders.iloc[:50_000].to_csv("part-0.csv", index=False)
orders.iloc[50_000:100_000].to_csv("part-1.csv", index=False)
orders.iloc[100_000:].to_csv("part-2.csv", index=False)

ddf = dd.read_csv("part-*.csv")
print(list(ddf.map_partitions(len).compute()))

means = ddf.map_partitions(lambda p: p["unit_price"].mean()).compute()
mean_of_means = round(float(means.mean()), 4)
print(mean_of_means)

true_mean = round(float(ddf["unit_price"].mean().compute()), 4)
print(true_mean)

print(mean_of_means == true_mean)
