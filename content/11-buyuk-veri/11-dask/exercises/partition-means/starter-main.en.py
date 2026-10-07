import dask.dataframe as dd
from orders_data import make_orders

orders = make_orders(120_000)

# Three files: 50 000, 50 000, 20 000.


# Partition sizes.


# The mean of partition means and dask's mean.
