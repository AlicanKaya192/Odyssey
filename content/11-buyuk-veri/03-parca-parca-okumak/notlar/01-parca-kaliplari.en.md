The patterns you need most often when reading in chunks. The skeleton is
always the same:

```python
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    # summarise in the chunk, add to the notebook
# at the end, get the result out of the notebook
```

## Total and count

```python
total = 0
rows = 0
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    total += chunk["unit_price"].sum()
    rows += len(chunk)
```

## Mean

**Not** the mean of means; the total and the count:

```python
mean = total / rows
```

## Minimum and maximum

```python
low = float("inf")
high = float("-inf")
for chunk in ...:
    low = min(low, chunk["unit_price"].min())
    high = max(high, chunk["unit_price"].max())
```

## Grouped total

```python
parts = []
for chunk in ...:
    parts.append(chunk.groupby("city")["unit_price"].sum())
result = pd.concat(parts).groupby(level=0).sum()
```

For a grouped mean, group the total and the count separately and divide at
the end:

```python
sums, counts = [], []
for chunk in ...:
    g = chunk.groupby("city")["unit_price"]
    sums.append(g.sum())
    counts.append(g.count())
mean = pd.concat(sums).groupby(level=0).sum() / pd.concat(counts).groupby(level=0).sum()
```

## Distinct values

```python
seen = set()
for chunk in ...:
    seen.update(chunk["customer_id"])
distinct = len(seen)
```

The set holds every different value; with many different values the set is
big too.

## The N largest rows

Take each chunk's N largest, then choose the N largest among those:

```python
tops = []
for chunk in ...:
    tops.append(chunk.nlargest(5, "unit_price"))
top = pd.concat(tops).nlargest(5, "unit_price")
```

The whole's 5 largest rows are bound to be among some chunk's 5 largest, so
the result is exact (on 300 000 rows it matched the all-at-once result).

## Filter and accumulate

```python
pieces = []
for chunk in ...:
    pieces.append(chunk[chunk["category"] == "electronics"])
result = pd.concat(pieces, ignore_index=True)
```

## Filter and append to a file

```python
first = True
for chunk in ...:
    part = chunk[chunk["quantity"] >= 4]
    part.to_csv("out.csv", mode="w" if first else "a", header=first, index=False)
    first = False
```

## Give types and columns in chunks too

```python
pd.read_csv("orders.csv", chunksize=100_000,
            usecols=["city", "quantity", "unit_price"],
            dtype={"city": "category", "quantity": "int8"})
```
