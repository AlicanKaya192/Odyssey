For each format, the line to write and read it, the useful options and the
measurement on this computer (a million orders).

## CSV

```python
df.to_csv("orders.csv", index=False)
pd.read_csv("orders.csv", usecols=[...], dtype={...}, parse_dates=[...])
```

61.1 MB · read 0.84 s · types are lost.

Without `index=False` the index goes into the file as an extra column.

## Compressed CSV

```python
df.to_csv("orders.csv.gz", index=False)     # it works it out from the extension
pd.read_csv("orders.csv.gz")
```

15.2 MB · write 3.5 s · read 0.92 s.

## JSON Lines

```python
df.to_json("orders.jsonl", orient="records", lines=True, date_format="iso")
pd.read_json("orders.jsonl", lines=True)
```

159.3 MB · read 3.25 s. `date_format="iso"` writes dates in a readable form
(`2024-01-02T22:15:01`).

## Parquet

```python
df.to_parquet("orders.parquet")                         # snappy
df.to_parquet("orders.parquet", compression="zstd")     # smaller
pd.read_parquet("orders.parquet")
pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
```

Snappy 20.9 MB, zstd 13.9 MB · read 0.02 s · types are kept.

## Feather

```python
df.to_feather("orders.feather")
pd.read_feather("orders.feather")
```

22.2 MB · write 0.03 s · read 0.02 s · types are kept.

## Deciding

| Question | Answer |
|---|---|
| Will a person or another program open it? | CSV |
| Is the data nested, or does it come from an API? | JSON Lines |
| Is it big, to be analysed, to be kept? | Parquet |
| Is it going to the next step on the same machine? | Feather |
| Is disk or network tight and CSV required? | CSV + gzip |
