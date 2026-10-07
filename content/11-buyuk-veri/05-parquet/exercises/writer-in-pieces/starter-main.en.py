import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 300_000)

# Read in chunks, write with a ParquetWriter.


# Close the writer.


# Rows and groups.


# The two quantity totals.
