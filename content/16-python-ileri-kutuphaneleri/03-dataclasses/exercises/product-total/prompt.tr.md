`Product` dataclass'ını tamamla: alanlar `name: str`, `price: float`,
`quantity: int = 1`; `total()` metodu `price * quantity` döndürsün. Sonra
`order_total(rows)` fonksiyonu `[ad, fiyat, adet]` satırlarından `Product`
nesneleri kurup tutarların toplamını `round(..., 2)` ile döndürsün.

**Beklenen çıktı:**

```
Product(name='pen', price=1.5, quantity=4)
18.0
```
