Yanında `sales.csv` var: sütunlar `date` (`2026-03-16` biçiminde) ve
`amount`. `sales_by_weekday(path)` fonksiyonunu yaz: `csv.DictReader` ile
okusun, her satırın gününü `date.fromisoformat(...).weekday()` ile bulup
`DAYS` listesinden adını alsın ve günlere göre toplamları (`round(..., 2)`)
sözlük olarak döndürsün.

**Beklenen çıktı:**

```
Mon 160.75
Tue 80.0
Sat 200.0
Sun 15.75
```
