`month_table(dates, stores, amounts)` tarihleri (`YYYY-MM-DD`) okuyup aya
çevirsin (`dt.to_period("M").astype(str)`) ve ay × mağaza **toplam** tablosu
kursun (`pivot_table(..., aggfunc="sum", fill_value=0)`). Şunu döndürsün:

- `"months"`: satırlardaki aylar (liste)
- `"values"`: tablo, liste listesi

**Döngü yazma.**

**Beklenen çıktı:**

```
['2026-01', '2026-02', '2026-03']
[[100, 50], [70, 0], [0, 30]]
```
