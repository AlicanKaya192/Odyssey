`invoice_total(rows, rate)` `[ad, "fiyat", adet]` satırlarının toplamını vergi
oranıyla (`rate`, metin) hesaplıyor ama `float` kullanıyor. Şöyle yeniden
yaz:

- Her satırı `Line` adlı bir `@dataclass`'a çevir (`name: str`,
  `price: Decimal`, `qty: int`).
- Ara toplamı `Decimal` ile hesapla, `(1 + Decimal(rate))` ile çarp.
- Sonucu `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` ile yuvarlayıp
  **metin** olarak döndür.

**Beklenen çıktı:**

```
34.12
```
