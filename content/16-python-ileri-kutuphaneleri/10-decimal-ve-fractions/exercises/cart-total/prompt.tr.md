`cart_total(prices)` fiyatları (`"19.99"` gibi metinler) topluyor ama
`float` kullandığı için `3.3000000000000003` gibi sonuçlar çıkıyor.
Fonksiyonu `Decimal` ile yeniden yaz; toplamı **metin** olarak (`str`)
döndürsün. Boş listede `"0"` döner.

**Beklenen çıktı:**

```
3.30
25.10
```
