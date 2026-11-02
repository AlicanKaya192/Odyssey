# Genel Tekrar

İstatistiksel Çıkarım modülünün sonuna geldin. Örneklemin evrenden farklı
olmasından başlayıp güven aralığına, hipotez testlerine, etki büyüklüğüne,
güç analizine ve Bayesçi bakışa kadar bir A/B testini okumak için gereken
bütün araçları gördün. Bu bölüm yolu bir kez daha yürüyor; sonunda baştan
sona bir A/B analizi var.

<figure class="fig">
  <div class="flow">
    <span class="node">Örneklem<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Aralık<br><small>05</small></span><span class="arrow">→</span>
    <span class="node">Test<br><small>06–12</small></span><span class="arrow">→</span>
    <span class="node">Etki ve güç<br><small>13–14</small></span><span class="arrow">→</span>
    <span class="node acc">Bayes<br><small>15</small></span>
  </div>
  <figcaption>Modülün yolu: önce belirsizliği görmek, sonra ölçmek, sınamak, büyüklüğünü söylemek ve son olarak başka bir gözle bakmak.</figcaption>
</figure>

## 1. Örneklem ve tahmin (Bölüm 0–4)

| Kavram | Akılda kalacak |
|---|---|
| Evren ve örneklem | parametre evrenin, istatistik örneklemin; her örneklem farklı cevap verir |
| Yanlı örneklem | büyütmek yanlılığı düzeltmez |
| Merkez ve yayılım | ortalama aykırıya duyarlı, medyan değil; sapmada n − 1 |
| Dağılımlar | binom (kaç başarı), Poisson (kaç olay), normal (çan) |
| Merkezi limit teoremi | ortalamaların dağılımı çan biçimine yaklaşır; çarpık veride daha geç |
| Standart hata | $s / \sqrt{n}$; hassasiyeti iki katına çıkarmak dört kat veri ister |

## 2. Güven aralığı (Bölüm 5)

Tahmin ± çarpan × standart hata. "%95" yöntemin tekrarlarda tutma oranıdır,
tek bir aralığın olasılığı değil. Küçük örneklemde t çarpanı, oranlar için
Wilson aralığı.

## 3. Hipotez testleri (Bölüm 6–12)

| Soru | Test | scipy / statsmodels |
|---|---|---|
| İki bağımsız ortalama | Welch t-testi | `stats.ttest_ind(b, a, equal_var=False)` |
| Eşli ölçümler | eşli t-testi | `stats.ttest_rel(before, after)` |
| İki oran | z-testi | `proportions_ztest([k_b, k_a], [n_b, n_a])` |
| Küçük sayılar | Fisher | `stats.fisher_exact(table)` |
| Dağılım / bağımsızlık | ki-kare | `stats.chisquare`, `stats.chi2_contingency` |
| Üç ve daha çok ortalama | ANOVA + Tukey | `stats.f_oneway`, `stats.tukey_hsd` |
| Çarpık veri, aykırılar | sıralı testler | `mannwhitneyu`, `wilcoxon`, `kruskal` |

p, "H₀ doğru olsaydı bu kadar uç bir sonuç ne sıklıkla çıkardı?" sorusunun
cevabıdır. H₀'ın olasılığı değildir, etkinin büyüklüğü değildir; çok
karşılaştırmada yanlış alarmlar birikir.

## 4. Etki büyüklüğü ve güç (Bölüm 13–14)

- Cohen's d ve h farkı standart bir ölçekte verir; risk farkı, göreli risk
  ve odds oranı oranları anlatır. Göreli risk taban oranıyla yazılır.
- Güç = gerçek etkiyi yakalama olasılığı. Etki, α, güç ve n'den üçü verilince
  dördüncüsü `solve_power` ile bulunur; n etkinin karesiyle ters orantılı.
- Düşük güçte anlamlı çıkan sonuçlar etkiyi abartır.

## 5. Bayesçi bakış (Bölüm 15)

Beta önsel + veri → Beta sonsal; P(B > A), inandırıcı aralık ve beklenen
kayıp karar vericinin doğrudan sorduğu sayılardır. Önsel önceden ve
gerekçesiyle seçilir.

## Baştan sona bir A/B testi

Sıra her zaman aynı: **önce plan, sonra veri.**

**1. Plan.** Taban satın alma oranı %11,4; ekip en az %13,0'a çıkmayı
anlamlı buluyor. Kaç kişi gerekir ve karar kuralı ne?

```python
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

h = proportion_effectsize(0.130, 0.114)
n_plan = NormalIndPower().solve_power(effect_size=h, power=0.8, alpha=0.05)
print(int(np.ceil(n_plan)))
```

```text
6562
```

Plan: grup başına 6600 kişi (biraz pay), iki yönlü z-testi, α = 0,05, pratik
eşik 1 puan. Bunlar test başlamadan yazılır.

**2. Analiz.** Test bitti:

```python
from statsmodels.stats.proportion import confint_proportions_2indep
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_checkout_test

shop = make_checkout_test(n=6600, seed=601)
k = shop.groupby("group")["bought"].sum()
rate_a, rate_b = k["A"] / 6600, k["B"] / 6600
p = proportions_ztest([k["B"], k["A"]], [6600, 6600])[1]
low, high = confint_proportions_2indep(k["B"], 6600, k["A"], 6600)
print(round(rate_a, 4), round(rate_b, 4))
print(f"{p:.1e}")
print(round(low, 4), round(high, 4))
```

```text
0.1106 0.1315
2.3e-04
0.0098 0.032
```

**3. Rapor.** "Yeni düğmede satın alma oranı %11,06 yerine
%13,15 oldu: 2,1 puan fark (%95 güven aralığı
0,98 – 3,20 puan, p = 2,3e-04). Fark büyük
olasılıkla gerçek. Aralığın alt ucu 1 puanlık eşiğin hemen altında olduğu
için eşiğin geçildiğini kesin söyleyemiyoruz."

Bu rapor, modülde gördüğün her şeyi kullanıyor: plan (güç), test (p),
aralık (belirsizlik), etki (puan farkı) ve pratik eşik. Tek bir p değeri
bunların hiçbirinin yerini tutmaz.
