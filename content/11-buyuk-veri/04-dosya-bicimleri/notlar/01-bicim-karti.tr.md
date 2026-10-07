Her biçim için yazma ve okuma satırı, işe yarayan seçenekler ve bu
bilgisayardaki ölçüm (bir milyon sipariş).

## CSV

```python
df.to_csv("orders.csv", index=False)
pd.read_csv("orders.csv", usecols=[...], dtype={...}, parse_dates=[...])
```

61,1 MB · okuma 0,84 sn · türler kayboluyor.

`index=False` yazılmazsa indeks fazladan bir sütun olarak dosyaya giriyor.

## Sıkıştırılmış CSV

```python
df.to_csv("orders.csv.gz", index=False)     # uzantıdan anlıyor
pd.read_csv("orders.csv.gz")
```

15,2 MB · yazma 3,5 sn · okuma 0,92 sn.

## JSON Lines

```python
df.to_json("orders.jsonl", orient="records", lines=True, date_format="iso")
pd.read_json("orders.jsonl", lines=True)
```

159,3 MB · okuma 3,25 sn. `date_format="iso"` tarihleri okunabilir
(`2024-01-02T22:15:01`) yazıyor.

## Parquet

```python
df.to_parquet("orders.parquet")                         # snappy
df.to_parquet("orders.parquet", compression="zstd")     # daha küçük
pd.read_parquet("orders.parquet")
pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
```

Snappy 20,9 MB, zstd 13,9 MB · okuma 0,02 sn · türler korunuyor.

## Feather

```python
df.to_feather("orders.feather")
pd.read_feather("orders.feather")
```

22,2 MB · yazma 0,03 sn · okuma 0,02 sn · türler korunuyor.

## Karar

| Soru | Cevap |
|---|---|
| Bir insan ya da başka bir program açacak mı? | CSV |
| Veri iç içe mi, bir API'den mi geliyor? | JSON Lines |
| Büyük mü, analiz edilecek mi, saklanacak mı? | Parquet |
| Aynı makinede bir sonraki adıma mı gidiyor? | Feather |
| Disk ya da ağ dar ve CSV şart mı? | CSV + gzip |
