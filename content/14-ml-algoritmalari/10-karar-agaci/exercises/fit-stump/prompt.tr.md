`fit_stump(X, y)` fonksiyonunu yaz: tek sorulu ağaç (karar kütüğü). Bütün
özellikler ve orta nokta eşikleri arasında ağırlıklı Gini'yi en küçük yapanı
bul (eşitlikte önce gelen özellik ve küçük eşik). `[özellik, eşik, sol etiket,
sağ etiket]` döndürsün; eşik `round(..., 4)`, etiketler o taraftaki çoğunluk
(eşitlikte küçük). `gini` hazır.

`DecisionTreeClassifier` yok.

**Beklenen çıktı:**

```
[0, 4.5, 0, 1]
```
