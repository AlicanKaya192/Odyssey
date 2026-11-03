## Üç düzeltme tek fonksiyonda

```python
from statsmodels.stats.multitest import multipletests

p = [0.001, 0.012, 0.021, 0.038, 0.3]
for method in ["bonferroni", "holm", "fdr_bh"]:
    reject, p_adj = multipletests(p, alpha=0.05, method=method)[:2]
    print(method, *reject.astype(int), *[round(float(x), 4) for x in p_adj])
```

```text
bonferroni 1 0 0 0 0 0.005 0.06 0.105 0.19 1.0
holm 1 1 0 0 0 0.005 0.048 0.063 0.076 0.3
fdr_bh 1 1 1 1 0 0.005 0.03 0.035 0.0475 0.3
```

Her satırda önce beş testin kararı (1 = kabul edilen bulgu), sonra
**düzeltilmiş p** değerleri. Düzeltilmiş p doğrudan 0,05 ile
karşılaştırılır: eşiği değiştirmek yerine p'yi büyütür.

## Elle hesap (m test, α = 0,05)

| Yöntem | Kural | Neyi korur |
|---|---|---|
| Bonferroni | p < α / m | ailece hata oranı (FWER) |
| Holm | sıralı k. p < α / (m − k + 1); ilk geçemeyende dur | FWER |
| Benjamini–Hochberg | sıralı k. p ≤ k · α / m olan en büyük k'ye kadar hepsi | yanlış keşif oranı (FDR) |

## Hatırlatmalar

- m, **bakılan** test sayısıdır; panoda görülüp yok sayılanlar da
  sayılır.
- Holm Bonferroni'den hiçbir zaman az bulmaz; ikisi aynı şeyi korur,
  Holm'u seçmek bedavadır.
- BH'nin "%5"i, bulguların içindeki yanlışların beklenen payıdır; tek bir
  yanlış alarm olasılığı değildir.
