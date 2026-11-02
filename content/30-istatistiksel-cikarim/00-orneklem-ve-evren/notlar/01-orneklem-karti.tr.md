| Terim | İngilizcesi | Anlamı |
|---|---|---|
| Evren | population | Hakkında konuştuğun grubun tamamı |
| Örneklem | sample | Evrenden seçip ölçtüğün kısım |
| Parametre | parameter | Evrenden hesaplanan sayı; genelde bilinmez |
| İstatistik | statistic | Örneklemden hesaplanan sayı |
| Çıkarım | inference | Örneklemden evren hakkında sonuç çıkarmak |
| Basit rastgele örneklem | simple random sample | Herkesin seçilme şansı eşit |
| Örnekleme hatası | sampling error | Şans yüzünden istatistiğin parametreden sapması |
| Yanlılık | bias | Seçim yüzünden hep aynı yöne sapma |
| Benzetim | simulation | Deneyi bilgisayarda binlerce kez tekrarlamak |

## Gösterim

| | Evren | Örneklem |
|---|---|---|
| Büyüklük | $N$ | $n$ |
| Ortalama | $\mu$ | $\bar{x}$ |
| Pay | $p$ | $\hat{p}$ |

## pandas ile örneklem

```python
from ab_data import make_population

users = make_population()
sample = users.sample(n=100, random_state=1)   # 100 kişi, tekrar yok
part = users["minutes"].sample(n=50, random_state=2)
```

- `random_state` aynı kalırsa aynı kişiler seçilir; sonuç tekrarlanabilir.
- `replace=False` varsayılandır: aynı kişi iki kez seçilmez.
- NumPy ile: `np.random.default_rng(seed).choice(values, size=n, replace=False)`.

## Akılda kalsın

- Tek örneklemin sonucu bir tahmindir, gerçeğin kendisi değil.
- Örneklemi büyütmek şansı azaltır, yanlılığı azaltmaz.
