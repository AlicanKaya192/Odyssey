`city_table(rows)` `[şehir, yıl, satış]` satırlarını (aynı şehir ve yıl
birden fazla kez geçebilir, bazı şehirlerin bazı yılları yok) şehir × yıl
tablosuna çevirsin: `groupby(["city", "year"])["sales"].sum()`, sonra
`unstack(fill_value=0)`. Şunu döndürsün:

- `"years"`: sütunlardaki yıllar (liste)
- `"cities"`: satırlardaki şehirler (liste)
- `"values"`: tablo, liste listesi (`.values.tolist()`)

**Döngü yazma.**

**Beklenen çıktı:**

```
[2024, 2025]
['Ankara', 'Bursa', 'Izmir']
[120, 110]
[50, 0]
[80, 95]
```
