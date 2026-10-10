`stack_months(months)` ay adı → `[şehir, satış]` satırları sözlüğü alıyor.
Her ayı bir DataFrame yapıp (`columns=["city", "sales"]`) **tek** bir
`pd.concat(..., keys=adlar)` çağrısıyla birleştirsin. Şunu döndürsün:

- `"rows"`: toplam satır sayısı
- `"index"`: `ignore_index=True` ile birleştirilmiş tablonun indeksi (liste)
- `"totals"`: ay başına toplam satış, ayların **verildiği sırayla**
  (`groupby(level=0, sort=False)`)

**Beklenen çıktı:**

```
6 [0, 1, 2, 3, 4, 5]
{'jan': 200, 'feb': 50, 'mar': 170}
```
