# Çoklu Karşılaştırma

Bir A/B testinin panosunda tek bir metrik durmaz: satın alma, gelir,
sepet büyüklüğü, tıklama, oturum süresi, iade... Her birine ayrı bir
test yapılır ve her biri %5 yanlış alarm şansı taşır. Bu bölüm, birçok
testi aynı anda okumanın neden tehlikeli olduğunu ölçüyor ve üç düzeltme
yöntemini gösteriyor.

## Yirmi metrik, beş "anlamlı" sonuç

Aynı deneyi 20 metrikle izleyen bir pano düşünelim. Veriyi biz ürettik,
bu yüzden gerçeği biliyoruz: B yalnızca ilk üç metriği gerçekten
değiştiriyor (`metric_01` %3, `metric_02` %2, `metric_03` %1,5); kalan
17 metrikte hiçbir etki yok.

```python
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from ab_data import make_metric_panel

panel = make_metric_panel()
metrics = [c for c in panel.columns if c.startswith("metric_")]


def metric_p(table):
    values = table[metrics].to_numpy()
    is_b = (table["group"] == "B").to_numpy()
    result = stats.ttest_ind(values[is_b], values[~is_b], equal_var=False)
    return result.pvalue


p = metric_p(panel)
print(*[m for m, x in zip(metrics, p) if x < 0.05])
```

```text
metric_01 metric_02 metric_03 metric_06 metric_20
```

Beş metrik %5 eşiğinin altında. Üçü gerçek, ama **ikisi** (`metric_06`
ve `metric_20`) şans eseri. Panoya bakan biri bu ikisini de "B bunu da
değiştirdi" diye okur.

## Neden olur?

Tek bir testte H₀ doğruysa yanlış alarm şansı %5'tir. Birbirinden
bağımsız 20 testte **en az bir** yanlış alarm şansı

$$1 - 0{,}95^{20} \approx 0{,}64$$

olur. Bunu hiçbir metriğin değişmediği 300 A/A panosunda ölçelim:

```python
any_alarm = 0
for s in range(300):
    p_aa = metric_p(make_metric_panel(seed=1000 + s, effect=False))
    any_alarm += (p_aa < 0.05).any()
print(any_alarm / 300, round(1 - 0.95 ** 20, 3))
```

```text
0.66 0.642
```

Hiçbir şeyin değişmediği panoların %66,0 kadarında en az bir
metrik "anlamlı" çıkıyor; formülün söylediği %64,2. Buna
**ailece hata oranı** (family-wise error rate, FWER) denir: bir test
ailesinde en az bir yanlış alarm olasılığı. Sıralı Bakma Tuzağı ve
Ardışık Test bölümünde aynı testi her gün okumak da bu sorundu; burada
aynı günü 20 metrikle okuyoruz.

## Üç düzeltme

`statsmodels` üç yaygın yöntemi tek fonksiyonla veriyor:

- **Bonferroni:** her p'yi α / m ile karşılaştır (m test sayısı). En
  basiti ve en sıkısı.
- **Holm:** p'leri küçükten büyüğe sırala; en küçüğü α / m, ikincisi
  α / (m − 1)... ile karşılaştır ve ilk geçemeyende dur. Ailece hata
  oranını Bonferroni kadar korur ama hiçbir zaman ondan az bulmaz.
- **Benjamini–Hochberg (BH):** başka bir şeyi korur: **yanlış keşif
  oranını** (false discovery rate, FDR), yani "anlamlı" denen metriklerin
  içinde yanlışların beklenen payını. Sıralı k. p'yi k · α / m ile
  karşılaştırır; eşiği tutan en büyük k'ye kadar hepsini kabul eder.

```python
for method in ["bonferroni", "holm", "fdr_bh"]:
    reject = multipletests(p, alpha=0.05, method=method)[0]
    print(method, *[m for m, r in zip(metrics, reject) if r])
```

```text
bonferroni metric_01
holm metric_01
fdr_bh metric_01
```

Üç yöntem de iki yanlış alarmı eliyor, ama gerçek etkili `metric_02` ve
`metric_03` de gidiyor: bu panoda yalnızca en büyük etki kalıyor.
Düzeltmenin bir bedeli var.

## Bedeli ölçmek

Tek bir panoya bakarak karar verilmez. 300 A/A panosunda (yanlış alarm)
ve ilk üç metriğin gerçekten değiştiği 300 panoda (gerçek ve yanlış
bulgular) dört kuralı karşılaştıralım:

```python
methods = ["none", "bonferroni", "holm", "fdr_bh"]


def rejects(p_values, method):
    if method == "none":
        return p_values < 0.05
    return multipletests(p_values, alpha=0.05, method=method)[0]


alarm = {m: 0 for m in methods}
found = {m: [] for m in methods}
for s in range(300):
    p_aa = metric_p(make_metric_panel(seed=5000 + s, effect=False))
    p_ab = metric_p(make_metric_panel(seed=3000 + s))
    for m in methods:
        alarm[m] += rejects(p_aa, m).any()
        r = rejects(p_ab, m)
        found[m].append([r[:3].sum(), r[3:].sum()])
for m in methods:
    real, false = np.mean(found[m], axis=0)
    print(m, round(alarm[m] / 300, 3), round(real, 2), round(false, 2))
```

```text
none 0.657 2.45 0.85
bonferroni 0.057 1.65 0.06
holm 0.057 1.67 0.06
fdr_bh 0.057 1.89 0.16
```

Sütunlar: A/A panolarında en az bir yanlış alarm, gerçek panolarda üç
gerçek etkiden ortalama kaç tanesi bulundu, ve kaç yanlış metrik
"anlamlı" çıktı.

- Düzeltmesiz okuma A/A panolarının %65,7 kadarında alarm
  veriyor ve her gerçek panoda ortalama 0,85 yanlış metrik
  ekliyor.
- Bonferroni ve Holm yanlış alarmı %5 civarına indiriyor; karşılığında
  üç gerçek etkiden ortalama 1,65 ve 1,67 tanesini
  buluyor.
- BH ortada duruyor: 1,89 gerçek etki buluyor, ama panoya
  ortalama 0,16 yanlış metrik de giriyor. A/A panosunda bütün
  H₀'lar doğru olduğu için FDR ile FWER aynı şeydir; bu yüzden orada BH
  de %5 civarında kalıyor.

Hangisi seçilir? Bu, yanlış bir "anlamlı"nın ne kadar pahalı olduğuna
bağlı. Her bulgunun bir ürün kararına dönüştüğü yerde Holm; birçok
metrikten "bakmaya değer" adayları seçilen keşif çalışmasında BH.

## En iyi düzeltme: daha az soru

Düzeltme yöntemleri ancak hasarı sınırlar. Asıl çare Deney Sorusu ve
Metrik Seçimi bölümünde gördüğümüz plandır:

- **Tek birincil metrik** önceden yazılır; karar ona göre verilir ve onun
  için düzeltme gerekmez.
- Koruma metrikleri "bozuldu mu" diye okunur; ikincil metrikler karar
  vermez, yalnızca açıklar.
- Birden çok varyant (A/B/C/D) da çoklu karşılaştırmadır: her varyantı
  kontrolle karşılaştırmak üç test eder.
- Test bittikten sonra metrik ya da segment aramak (Segmentler ve Simpson
  Paradoksu bölümü) aynı tuzaktır: yeterince arayan bir "anlamlı" bulur.

## Özet

- m testte en az bir yanlış alarm olasılığı 1 − (1 − α)^m; 20 testte
  yaklaşık %64.
- Bonferroni ve Holm ailece hata oranını, BH yanlış keşif oranını korur.
- Düzeltme gerçek etkileri de kaçırır; bedeli benzetimle ölçülür.
- En iyi çare önceden yazılmış tek birincil metriktir.
