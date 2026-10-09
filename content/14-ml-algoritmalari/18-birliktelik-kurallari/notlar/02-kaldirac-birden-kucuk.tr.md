Derste güven eşiği 0,5 idi; bu eşik, kaldıracı 1'in altındaki kuralları hiç
göstermez. Oysa veriyi üretirken çayı kahveye **ters** bağlamıştık: kahve
varken çay daha az olası. Bu ilişkiyi sık kümelerden doğrudan okuyalım
(dersteki `freq` ve `baskets` ile):

```python
coffee, tea = frozenset(["coffee"]), frozenset(["tea"])
both = freq[coffee | tea]
conf = both / freq[coffee]
print(round(freq[tea], 3), round(conf, 3), round(conf / freq[tea], 2))
no_coffee = [b for b in baskets if "coffee" not in b]
print(round(sum("tea" in b for b in no_coffee) / len(no_coffee), 3))
```

```text
0.301 0.14 0.46
0.397
```

Bütün sepetlerin %30,1'inde çay var, ama kahve alanların yalnızca %14'ünde:
kaldıraç 0,46. Kahve almayanlarda bu oran %39,7. İkisi birbirinin yerine
geçiyor (ikame ürünler, substitutes).

Bu kural da işe yarar bilgi: kahve alana çay önermek muhtemelen boşa gider ve
kampanya planlanırken iki ürünün birbirinin yerine geçtiği hesaba katılmalı. Güven eşiğiyle süzen
bir kural madencisi bunu hiç göstermez; kaldıracı 1'in **altında** kalan
kurallara ayrıca bakmak gerekir.
