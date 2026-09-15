İptal edilmeyen siparişlerde her ay, her kategorinin cirosunu ve **o
ayın** toplam cirosundaki yüzde payını göster.

Sütunlar: `month` (ayın ilk günü), `category_code`, `revenue`, `share`
(`DECIMAL(5,2)`). `month`, sonra `revenue` (büyükten küçüğe) ile sırala.

```
month       category_code  revenue   share
----------  -------------  --------  -----
2026-01-01  COM            24500.00  74.89
2026-01-01  DIS            6400.00   19.56
2026-01-01  ACC            1815.00   5.55
2026-02-01  COM            18900.00  65.90
...
```

Her ayın payları kendi içinde 100 ediyor. Kullandığın bölümler: tabloları
birleştirmek (06), gruplama (05), tarih (10), `WITH` (12), pencere (11).
