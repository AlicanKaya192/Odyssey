## Her kolun en iyi olma olasılığı

```python
import numpy as np

rng = np.random.default_rng(0)
k = np.array([12, 30, 25])
n = np.array([300, 500, 400])
draws = rng.beta(1 + k, 1 + n - k, (20000, 3))
best = draws.argmax(axis=1)
print([round(float((best == j).mean()), 3) for j in range(3)])
```

```text
[0.044, 0.413, 0.543]
```

Thompson örneklemesi bir sonraki ziyaretçiyi kollara tam bu olasılıklarla
dağıtır: en iyi olma olasılığı yüksek olan kol daha çok ziyaretçi alır.

## Üç yaygın yöntem

| Yöntem | Nasıl seçer | Not |
|---|---|---|
| ε-açgözlü (epsilon-greedy) | ε olasılıkla rastgele kol, yoksa en iyi görünen | basit; ε elle seçilir |
| UCB | tahmin + belirsizlik payı en büyük olan | az denenen kola pay verir |
| Thompson örneklemesi | her kolun dağılımından bir değer çek, en büyüğü | ayarı az, pratikte iyi |

## Sözlük

- **Kol (arm):** bir seçenek.
- **Keşif / kullanım:** az bilinen kolu denemek / en iyi görüneni seçmek.
- **Pişmanlık (regret):** en iyi kola göre kaybedilen kazanç.
