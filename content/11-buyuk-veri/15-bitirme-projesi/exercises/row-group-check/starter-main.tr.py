import duckdb
import pyarrow.parquet as pq
from orders_data import make_orders

make_orders(500_000).to_parquet("orders.parquet", row_group_size=100_000, index=False)
pf = pq.ParquetFile("orders.parquet")
counts = {}
revenue = {}

# 2. Satir gruplarindan kismi toplamlar.


# 3. Sonuclar.


# 4. DuckDB ile karsilastirma.
