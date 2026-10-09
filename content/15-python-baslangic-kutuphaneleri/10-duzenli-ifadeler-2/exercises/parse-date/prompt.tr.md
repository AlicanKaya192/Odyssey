`parse_date(text)` fonksiyonunu yaz: metindeki **ilk** `gg.aa.yyyy`
biçimindeki tarihi bulsun ve `(yıl, ay, gün)` demetini **tam sayı** olarak
döndürsün; tarih yoksa `None`. Üç grup kullan: `(\d{2})\.(\d{2})\.(\d{4})`.

**Beklenen çıktı:**

```
(2026, 3, 15)
None
```
