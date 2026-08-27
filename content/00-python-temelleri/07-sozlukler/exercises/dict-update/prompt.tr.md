Bir stok sözlüğü verilmiş:

```python
stock = {"apple": 10, "banana": 5}
```

İki işlem yap:

- `cherry` diye **yeni bir ürün** ekle, adedi `20` olsun.
- `apple` ürününün adedini `15` olarak **güncelle**.

Sonra sözlüğü ve kaç çeşit ürün olduğunu yazdır. Beklenen çıktı:

```
{'apple': 15, 'banana': 5, 'cherry': 20}
3
```

> Sözlükte ekleme ve güncelleme **aynı satırla** yapılıyor: `stock[anahtar] = deger`.
> Anahtar yoksa ekler, varsa değerini değiştirir. Listedeki `append` gibi ayrı
> bir metoda gerek yok.
