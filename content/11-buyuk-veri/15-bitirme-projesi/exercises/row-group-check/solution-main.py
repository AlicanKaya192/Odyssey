import duckdb
import pyarrow.parquet as pq
from orders_data import make_orders

make_orders(500_000).to_parquet("orders.parquet", row_group_size=100_000, index=False)
pf = pq.ParquetFile("orders.parquet")
counts = {}
revenue = {}

for i in range(pf.num_row_groups):
    part = pf.read_row_group(i, columns=["payment", "quantity", "unit_price"]).to_pandas()
    part["revenue"] = part["quantity"] * part["unit_price"]
    summary = part.groupby("payment")["revenue"].agg(["count", "sum"])
    for payment, row in summary.iterrows():
        counts[payment] = counts.get(payment, 0) + int(row["count"])
        revenue[payment] = revenue.get(payment, 0.0) + row["sum"]

for payment in sorted(counts):
    print(payment, counts[payment], round(revenue[payment], 2))

exact = duckdb.sql("""
    SELECT payment, count(*), sum(quantity * unit_price)
    FROM 'orders.parquet'
    GROUP BY payment
""").fetchall()
same = all(counts[p] == n and abs(revenue[p] - r) < 0.01 for p, n, r in exact)
print(same)
