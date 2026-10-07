import duckdb
from orders_data import make_orders

make_orders(100_000).to_parquet("orders.parquet", index=False)

# Connect, build the orders and city_summary tables.


# Write city_summary to CSV, close.


# Connect again: number of rows in orders.


# The first three lines of the CSV.
