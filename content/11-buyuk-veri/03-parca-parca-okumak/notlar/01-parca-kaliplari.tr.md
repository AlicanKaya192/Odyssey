Parça parça okurken en sık gereken kalıplar. Hepsinde iskelet aynı:

```python
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    # parçada özetle, not defterine ekle
# en sonda not defterinden sonucu çıkar
```

## Toplam ve sayı

```python
total = 0
rows = 0
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    total += chunk["unit_price"].sum()
    rows += len(chunk)
```

## Ortalama

Ortalamaların ortalaması **değil**; toplam ve sayı:

```python
mean = total / rows
```

## En küçük ve en büyük

```python
low = float("inf")
high = float("-inf")
for chunk in ...:
    low = min(low, chunk["unit_price"].min())
    high = max(high, chunk["unit_price"].max())
```

## Gruplu toplam

```python
parts = []
for chunk in ...:
    parts.append(chunk.groupby("city")["unit_price"].sum())
result = pd.concat(parts).groupby(level=0).sum()
```

Gruplu ortalama için toplamı ve sayıyı ayrı ayrı grupla, sonda böl:

```python
sums, counts = [], []
for chunk in ...:
    g = chunk.groupby("city")["unit_price"]
    sums.append(g.sum())
    counts.append(g.count())
mean = pd.concat(sums).groupby(level=0).sum() / pd.concat(counts).groupby(level=0).sum()
```

## Farklı değerler

```python
seen = set()
for chunk in ...:
    seen.update(chunk["customer_id"])
distinct = len(seen)
```

Küme her farklı değeri tutuyor; farklı değer çoksa küme de büyük.

## En büyük N satır

Her parçanın en büyük N'ini al, sonra bunların arasından en büyük N'i seç:

```python
tops = []
for chunk in ...:
    tops.append(chunk.nlargest(5, "unit_price"))
top = pd.concat(tops).nlargest(5, "unit_price")
```

Bütünün en büyük 5 satırı mutlaka bir parçanın en büyük 5'i arasında; bu
yüzden sonuç kesin (300 000 satırda tek seferdekiyle aynı çıktı).

## Süz ve biriktir

```python
pieces = []
for chunk in ...:
    pieces.append(chunk[chunk["category"] == "electronics"])
result = pd.concat(pieces, ignore_index=True)
```

## Süz ve dosyaya ekle

```python
first = True
for chunk in ...:
    part = chunk[chunk["quantity"] >= 4]
    part.to_csv("out.csv", mode="w" if first else "a", header=first, index=False)
    first = False
```

## Türleri ve sütunları parçada da ver

```python
pd.read_csv("orders.csv", chunksize=100_000,
            usecols=["city", "quantity", "unit_price"],
            dtype={"city": "category", "quantity": "int8"})
```
