`dates` ISO tarihli yedekler, `today` bugünün ISO tarihi.
`gfs_keep(dates, today)` saklanacak yedeklerin tarihlerini küçükten büyüğe
döndürsün. Bir yedek saklanır, eğer:

- 7 günden yeni ise (yaş `< 7`),
- Pazar günüyse (`weekday() == 6`) ve 28 günden yeniyse,
- ayın ilk günüyse.

**Beklenen çıktı:**

```
11
2026-10-01
2026-10-11
2026-10-18
2026-10-25
2026-10-26
```
