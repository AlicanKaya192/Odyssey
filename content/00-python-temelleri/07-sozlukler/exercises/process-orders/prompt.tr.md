Bir dükkânın stoku ve gelen siparişler:

```python
stock = {"apple": 10, "pear": 4, "plum": 0}
orders = [("apple", 3), ("pear", 5), ("plum", 1), ("kiwi", 2), ("apple", 6)]
```

Siparişleri **sırayla** işle. Her sipariş için:

- Ürün stokta hiç yoksa (sözlükte anahtarı yoksa): `unknown` listesine
  ekle ve `kiwi: unknown product` yaz.
- Stok yetiyorsa: stoktan düş ve `apple: sent 3` yaz.
- Stok yetmiyorsa: **hiçbir şey gönderme**, eksik miktarı `shortages`
  sözlüğüne yaz ve `pear: short by 1` yaz.

En sonda kalan stoku yazdır:

```
apple: sent 3
pear: short by 1
plum: short by 1
kiwi: unknown product
apple: sent 6
Stock: {'apple': 1, 'pear': 4, 'plum': 0}
```

Her siparişin sonucu bir öncekine bağlı: ilk elma siparişi stoğu 7'ye
düşürüyor, son elma siparişi o 7'ye bakıyor.

> Dikkat: Stok yetmeyen siparişte stoğa dokunma; `pear` 4 olarak kalmalı.
> Her sipariş bir demet; `for product, amount in orders:` ile iki parçasını
> ayrı değişkenlere alabilirsin.
