import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 400_000)
NUMERIC = {"order_id": "int32", "customer_id": "int32", "quantity": "int8"}
MB = 1024**2

writer = None
for chunk in pd.read_csv("orders.csv", chunksize=100_000, dtype=NUMERIC):
    chunk["month"] = chunk["order_time"].str[:7]
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter("orders.parquet", table.schema, compression="zstd")
    writer.write_table(table)
writer.close()

pf = pq.ParquetFile("orders.parquet")
print(pf.metadata.num_rows)
print(pf.num_row_groups)
print(round(os.path.getsize("orders.csv") / MB, 1), round(os.path.getsize("orders.parquet") / MB, 1))

months = pd.read_parquet("orders.parquet", columns=["month"])
print(months["month"].nunique())
