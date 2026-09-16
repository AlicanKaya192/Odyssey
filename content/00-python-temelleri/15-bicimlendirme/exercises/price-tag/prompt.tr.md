Bir ürünün fiyatını, vergisini ve toplamını **kuruşuyla** yazdıracaksın.

Elindeki veri:

```python
price = 12.5
tax_rate = 0.18
```

**Yapman gerekenler:**

1. `tax` — verginin tutarı (`price * tax_rate`).
2. `total` — vergili fiyat.
3. Üçünü aşağıdaki gibi, **iki ondalık basamakla** yazdır.

**Beklenen çıktı:**

```
Price: 12.50
Tax: 2.25
Total: 14.75
```

> `round()` kullanma. Biçim belirteci hem yuvarlıyor hem de sondaki sıfırı
> yazıyor: `f"{price:.2f}"`.
