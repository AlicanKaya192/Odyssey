`allowed_downtime(percent, days)` fonksiyonunu yaz: `days` günlük bir
dönemde, `percent` erişilebilirlik sözü ne kadar kesintiye izin veriyor?

- Önce izin verilen dakikayı hesapla: `days * 24 * 60 * (1 - percent / 100)`.
- Bunu en yakın tam dakikaya yuvarla (`round`).
- Sonucu `(saat, dakika)` demeti olarak döndür. `divmod(n, 60)` ikisini
  birlikte verir.

**Beklenen çıktı:**

```
(0, 43)
(87, 36)
(0, 53)
```
