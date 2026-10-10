`parse_dates(texts)` `gün.ay.yıl` yazılmış metinleri tarihe çevirsin
(`format="%d.%m.%Y"`, `errors="coerce"`). Okunamayanların sayısını ve
okunabilenleri `YYYY-MM-DD` metni olarak döndürsün:
`{"bad": sayı, "dates": [...]}`. 31 Şubat gibi var olmayan bir gün de
okunamaz sayılır. **Döngü yazma.**

**Beklenen çıktı:**

```
2
['2026-03-02', '2026-03-15']
```
