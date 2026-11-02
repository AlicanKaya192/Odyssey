## İki test

| Test | Soru | scipy | Serbestlik derecesi |
|---|---|---|---|
| Uyum iyiliği | Sayımlar beklenen dağılıma uyuyor mu? | `stats.chisquare(gözlenen, f_exp=beklenen)` | kategori − 1 |
| Bağımsızlık | İki kategorik değişken ilişkili mi? | `stats.chi2_contingency(tablo)` | (satır − 1)(sütun − 1) |

## Eşit olmayan beklenti

Beklenen dağılım eşit değilse `f_exp` verilir. Toplamı gözlenenlerin
toplamına eşit olmalı:

```python
from scipy import stats

observed = [182, 174, 195, 172, 217, 216, 244]
shares = [0.13, 0.13, 0.13, 0.13, 0.14, 0.17, 0.17]
expected = [s * sum(observed) for s in shares]
result = stats.chisquare(observed, f_exp=expected)
print(round(result.statistic, 2), round(result.pvalue, 4))
```

```text
6.26 0.3942
```

Hafta sonuna daha çok sipariş bekleyen bir modelle aynı veri artık
şaşırtıcı değil: p büyük.

## Formüller

- $\chi^2 = \sum (G - B)^2 / B$
- Bağımsızlıkta beklenen: satır toplamı × sütun toplamı / genel toplam
- Cramér's V: `stats.contingency.association(tablo, method="cramer")`

## Kontrol listesi

- Tabloda sayımlar var, yüzdeler değil.
- Beklenen sayıların hepsi ≥ 5.
- 2×2'de `correction=False` z-testiyle aynı sonucu verir; varsayılan Yates
  düzeltmesi biraz tutucudur.
