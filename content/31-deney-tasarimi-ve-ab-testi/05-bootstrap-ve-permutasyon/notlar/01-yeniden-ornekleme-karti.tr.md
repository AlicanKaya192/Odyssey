## İki grup için bootstrap aralığı

```python
import numpy as np


def boot_ci(a, b, stat, reps=2000, seed=0):
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a), np.asarray(b)
    values = [stat(rng.choice(b, len(b))) - stat(rng.choice(a, len(a)))
              for _ in range(reps)]
    low, high = np.percentile(values, [2.5, 97.5])
    return round(float(low), 2), round(float(high), 2)


a = [12, 15, 9, 30, 14, 11, 13, 50, 10, 12]
b = [16, 18, 12, 35, 15, 17, 14, 60, 13, 16]
print(boot_ci(a, b, np.mean))
print(boot_ci(a, b, np.median))
```

```text
(-7.8, 15.3)
(-6.0, 12.5)
```

`stat` olarak ortalama, medyan ya da herhangi bir fonksiyon verilir.

## Permütasyon testi

1. Gerçek farkı hesapla.
2. Grup etiketlerini karıştır (`rng.permutation`), farkı yeniden hesapla.
3. Binlerce kez tekrarla.
4. p = |karıştırılmış fark| ≥ |gerçek fark| olanların payı.

## Ne zaman hangisi?

| Durum | Araç |
|---|---|
| Büyük örneklem, ortalama ya da oran | formül (Welch, z) |
| Formülü olmayan istatistik | bootstrap |
| Dağılım varsayımı istemeyen test | permütasyon |
| Küçük, çok çarpık örneklem | hiçbiri tam güvenilir değil; daha çok veri |

## Dikkat

- Yeniden örnekleme **atama biriminde** yapılır: kullanıcıyla atandıysa
  kullanıcılar örneklenir, sayfa gösterimleri değil.
- Tohum sabitlenir; sonuç tekrar üretilebilir olsun.
- 2000 tekrar aralık için genellikle yeter; küçük p için daha çok.
