## Adımlar

1. Soruyu ve $H_0$ / $H_1$'i yaz.
2. Yönü (iki ya da tek yönlü) ve $\alpha$'yı veriye bakmadan seç.
3. Test istatistiğini ve p değerini hesapla.
4. $p < \alpha$ ise $H_0$'ı reddet; değilse "reddedilemedi" de.
5. Etkiyi ve güven aralığını da raporla.

## Terimler

| Terim | İngilizcesi | Anlamı |
|---|---|---|
| Sıfır hipotezi | null hypothesis ($H_0$) | "Fark yok / etki yok" |
| Alternatif hipotez | alternative hypothesis ($H_1$) | "Fark var" |
| Test istatistiği | test statistic | Farkın standart hata cinsinden ölçüsü |
| p değeri | p-value | $H_0$ doğruysa en az bu kadar uç sonuç olasılığı |
| Anlamlılık düzeyi | significance level ($\alpha$) | Önceden seçilen eşik |
| I. tür hata | type I error | Yanlış alarm; olasılığı $\alpha$ |
| II. tür hata | type II error | Kaçırma; olasılığı $\beta$ |
| Güç | power | $1 - \beta$ |

## Tek örneklem t-testi

```python
from scipy import stats

loads = [910, 860, 845, 930, 880, 905, 870, 925]
two = stats.ttest_1samp(loads, 850)
one = stats.ttest_1samp(loads, 850, alternative="greater")
print(round(two.statistic, 3), round(two.pvalue, 4), round(one.pvalue, 4))
```

```text
3.667 0.008 0.004
```

- `alternative`: `"two-sided"` (varsayılan), `"greater"`, `"less"`.
- Tek yönlü p, sonuç beklenen yöndeyse iki yönlünün yarısıdır.

## Karar tablosu

| | $H_0$ doğru | $H_0$ yanlış |
|---|---|---|
| Reddet | I. tür hata ($\alpha$) | doğru (güç) |
| Reddetme | doğru | II. tür hata ($\beta$) |
