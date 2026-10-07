import duckdb
from orders_data import make_orders

make_orders(100_000).to_parquet("orders.parquet", index=False)

# One query: number of orders, distinct cities, total quantity.


# The three values, on separate lines.
