Neden çok ağaç tek ağaçtan iyi? Her biri %60 doğru olan ve hataları
birbirinden **tamamen bağımsız** `n` model düşünelim. Çoğunluk oyu,
modellerin yarıdan fazlası doğruysa doğrudur; bu bir binom olasılığı:

```python
from math import comb

for n in (1, 5, 25, 101):
    wins = range(n // 2 + 1, n + 1)
    acc = sum(comb(n, k) * 0.6 ** k * 0.4 ** (n - k) for k in wins)
    print(n, round(acc, 3))
```

```text
1 0.6
5 0.683
25 0.846
101 0.979
```

Tek başına %60 olan modellerden 101 tanesinin oyu %97,9 doğru. Bu, en iyi
durumun hesabı: gerçek ağaçların hataları bağımsız değil, aynı veriden
öğrendikleri için çoğu aynı örnekte yanılıyor. Derste 100 ağaçlı bagging tek
ağacı yalnızca 0,738'den 0,80'e taşıdı.

Topluluk yöntemlerinin bütün hüneri, hataları **olabildiğince bağımsız**
kılmak: farklı önyükleme örnekleri (bagging), farklı özellik alt kümeleri
(rastgele orman), ya da bir sonraki bölümde olduğu gibi her yeni modeli
öncekilerin hatalarına odaklamak (boosting).
