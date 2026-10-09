Yanında `sales.csv` var; sütunları `date`, `customer`, `city`, `amount`. Bazı şehirler virgül içeriyor (`"London, UK"`).

`total_by(path, key, value)` fonksiyonunu yaz: her `key` değeri için `value`
sütununun toplamını (`float`) sözlük olarak döndürsün; toplamlar
`round(..., 2)`. Örnek: `total_by("sales.csv", "customer", "amount")`.

**Beklenen çıktı:**

```
Ada 180.5
Alan 80.0
Grace 200.25
Linus 45.0
```
