Bloom filtresini kurmadan önce iki şeyi bilmek gerekir: kaç öğe (`n`)
geleceği ve hangi yanlış pozitif oranına (`p`) razı olduğun. Gereken bit sayısı
ve hash sayısı bunlardan hesaplanır:

- `m = −n · ln p / (ln 2)²` bit
- `k = (m / n) · ln 2` hash

```python
import math


def bloom_size(n, p):
    m = math.ceil(-n * math.log(p) / math.log(2) ** 2)
    k = round(m / n * math.log(2))
    return m, k


for n, p in [(1_000_000, 0.01), (1_000_000, 0.001), (100_000_000, 0.01)]:
    m, k = bloom_size(n, p)
    print(n, p, round(m / 8 / 1_000_000, 1), "MB", k, "hashes")
```

```text
1000000 0.01 1.2 MB 7 hashes
1000000 0.001 1.8 MB 10 hashes
100000000 0.01 119.8 MB 7 hashes
```

Bir milyon öğe için %1 hata 1,2 MB; hatayı on kat azaltmak belleği yalnızca
yaklaşık 1,5 kat artırıyor. Öğe başına yaklaşık 10 bit %1 hata için yeter, ve
bu öğelerin ne kadar uzun olduğundan **bağımsız**: bir milyon uzun adresi
kümede tutmak yüz megabaytı geçerdi.

Derste `n = 10 000`, `m = 100 000` (öğe başına 10 bit) ve `k = 7` seçilmişti:
formülün önerdiği değerlerin aynısı.
