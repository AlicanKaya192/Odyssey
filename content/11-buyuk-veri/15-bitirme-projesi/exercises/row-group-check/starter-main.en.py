import duckdb
import pyarrow.parquet as pq
from orders_data import make_orders

make_orders(500_000).to_parquet("orders.parquet", row_group_size=100_000, index=False)
pf = pq.ParquetFile("orders.parquet")
counts = {}
revenue = {}

# 2. Partial totals from the row groups.


# 3. The results.


# 4. Comparing with DuckDB.
