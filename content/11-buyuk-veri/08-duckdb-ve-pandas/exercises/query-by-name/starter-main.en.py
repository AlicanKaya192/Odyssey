import duckdb
from orders_data import make_orders

df = make_orders(100_000)

# FROM df: orders per payment method.
