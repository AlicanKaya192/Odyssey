`add_months(text, n)` fonksiyonunu yaz: `"2026-01-31"` biçimindeki tarihe
`n` ay eklesin (`n` negatif olabilir) ve sonucu aynı biçimde metin olarak
döndürsün. Gün yeni ayda yoksa ayın son gününe insin
(`calendar.monthrange(yıl, ay)[1]`).

**Beklenen çıktı:**

```
2026-02-28
2027-02-15
2026-02-28
```
