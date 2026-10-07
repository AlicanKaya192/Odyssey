import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 300_000)

writer = None
for chunk in pd.read_csv("orders.csv", chunksize=100_000, parse_dates=["order_time"]):
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter("orders.parquet", table.schema)
    writer.write_table(table)

writer.close()

meta = pq.ParquetFile("orders.parquet").metadata
print(meta.num_rows, meta.num_row_groups)

csv_total = pd.read_csv("orders.csv", usecols=["quantity"])["quantity"].sum()
parquet_total = pd.read_parquet("orders.parquet", columns=["quantity"])["quantity"].sum()
print(csv_total, parquet_total)
