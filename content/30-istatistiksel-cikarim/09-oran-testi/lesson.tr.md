# Oranları Karşılaştırmak

A/B testlerinde en sık sorulan soru bir ortalama değil, bir **oran**
hakkındadır: yeni ödeme düğmesi alışveriş yapanların payını artırdı mı?
Kayıt olanların, tıklayanların, geri dönenlerin payı ... Hepsinde her
kullanıcı için tek bir evet/hayır (1/0) vardır. Bu bölümde iki oranı
karşılaştırmayı, farkın güven aralığını kurmayı ve sayılar küçükken neden
başka bir teste geçmek gerektiğini öğreniyoruz.

## Veri: ödeme düğmesi testi

```python
from ab_data import make_checkout_test

test = make_checkout_test()
groups = test.groupby("group")["bought"]
k, n = groups.sum(), groups.count()
print(k.to_dict(), n.to_dict())
pa, pb = k["A"] / n["A"], k["B"] / n["B"]
print(round(pa, 4), round(pb, 4), round(pb - pa, 4), round((pb - pa) / pa, 3))
```

```text
{'A': 472, 'B': 560} {'A': 4000, 'B': 4000}
0.118 0.14 0.022 0.186
```

- Her grupta 4 000 kullanıcı. Eski düğmede (A) alışveriş yapanların payı
  0,118, yenisinde (B) 0,140.
- **Mutlak fark** (absolute difference): 0,022, yani yaklaşık 2,2
  yüzde puan.
- **Göreli artış** (relative lift): farkın A'ya oranı, %18,6.
  "Satışlar %19 arttı" cümlesi göreli artıştır; "yüzde puan" ile karıştırma.

## İki oran z-testi

$H_0$: iki grubun gerçek oranı aynı. $H_0$ doğruysa iki grubu tek bir
havuz gibi düşünebiliriz; ortak oran $\hat{p}$ iki grubun birleşiminden
gelir. Farkın standart hatası ve test istatistiği:

$$SE = \sqrt{\hat{p}(1-\hat{p})\left(\dfrac{1}{n_A} + \dfrac{1}{n_B}\right)} \qquad z = \dfrac{\hat{p}_B - \hat{p}_A}{SE}$$

```python
import numpy as np
from scipy import stats
from ab_data import make_checkout_test

test = make_checkout_test()
groups = test.groupby("group")["bought"]
k, n = groups.sum(), groups.count()
pa, pb = k["A"] / n["A"], k["B"] / n["B"]
pool = k.sum() / n.sum()
se = np.sqrt(pool * (1 - pool) * (1 / n["A"] + 1 / n["B"]))
z = (pb - pa) / se
print(round(pool, 4), round(se, 5), round(z, 3))
print(round(2 * stats.norm.sf(abs(z)), 4))
```

```text
0.129 0.0075 2.935
0.0033
```

- Ortak oran 0,1290, farkın standart hatası 0,0075. Fark
  standart hatanın yaklaşık 2,9 katı.
- İki yönlü p = 0,0033: `2 * sf(|z|)`, çünkü iki kuyruğa da bakıyoruz.

`statsmodels` aynı testi tek satırda yapar:

```python
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_checkout_test

test = make_checkout_test()
groups = test.groupby("group")["bought"]
k, n = groups.sum(), groups.count()
z, p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])
print(round(z, 3), round(p, 4))
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"],
                                       method="newcomb")
print(round(low, 4), round(high, 4))
```

```text
2.935 0.0033
0.0073 0.0367
```

- z ve p elle bulduğumuzla aynı.
- Farkın %95 güven aralığı 0,0073 ile 0,0367: yeni düğme
  alışveriş payını büyük olasılıkla 0,7 ile 3,7 yüzde puan arasında
  artırıyor. `method="newcomb"`, tek oran bölümündeki Wilson aralığının
  iki oranlı karşılığı; küçük örneklemde de güvenilir.
- Veriyi biz ürettik: gerçek fark 13,0 − 11,4 = 1,6 yüzde puan. Aralık onu
  içeriyor; gözlenen 2,2 şans yüzünden biraz büyük.

## Sayılar küçükken: Fisher'ın kesin testi

z-testi merkezi limit teoremine dayanır: oranların çan biçiminde dağıldığını
varsayar. Gruplar küçük ve olaylar seyrekse (birkaç alışveriş) bu varsayım
zayıflar. Küçük bir pilot testte 40'ar kişiden 3 ve 11 kişi alışveriş
yapmış olsun:

```python
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

table = [[3, 37], [11, 29]]
z, p_z = proportions_ztest([11, 3], [40, 40])
fisher = stats.fisher_exact(table)
print(round(p_z, 4), round(fisher.pvalue, 4))
```

```text
0.0186 0.0367
```

**Fisher'ın kesin testi** (Fisher's exact test) yaklaşık bir dağılım
kullanmaz; 2×2 tablonun bütün olası dizilişlerini sayar. Burada z-testi
p = 0,0186, Fisher p = 0,0367 verdi. Hangisi doğru davranıyor?
Gerçek farkın sıfır olduğu (ikisi de %8) küçük testleri 10 000 kez
benzetelim:

```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(131)
p_z, p_f = [], []
for _ in range(10000):
    a, b = rng.binomial(40, 0.08), rng.binomial(40, 0.08)
    if a + b == 0:
        p_z.append(1.0)
        p_f.append(1.0)
        continue
    p_z.append(proportions_ztest([b, a], [40, 40])[1])
    p_f.append(stats.fisher_exact([[a, 40 - a], [b, 40 - b]]).pvalue)
p_z, p_f = np.array(p_z), np.array(p_f)
print(round((p_z < 0.05).mean(), 4), round((p_f < 0.05).mean(), 4))
```

```text
0.0616 0.0157
```

- Fark yokken z-testi %6,2 oranında yanlış alarm verdi: söz
  verilen %5'in üstünde.
- Fisher %1,6: %5'in çok altında. Fisher **tutucudur**
  (conservative): yanlış alarmı sözünden az verir, bunun bedeli de güç
  kaybıdır.
- Kural: beklenen sayıların bir hücrede 5'in altına düştüğü küçük
  tablolarda Fisher, binlerce kullanıcılı A/B testlerinde z-testi.

## Raporlarken

- İki oranı, mutlak farkı (yüzde puan) ve göreli artışı birlikte ver.
- Farkın güven aralığını mutlak farka göre yaz: "+2,2 yüzde puan (%95 GA:
  0,7 ile 3,7)".
- Göreli artış küçük taban oranlarında çok büyük görünür: %1'den %2'ye çıkış
  "%100 artış"tır ama yalnızca 1 yüzde puandır.

## Özet

- Oran, 0/1 verinin ortalamasıdır; iki oran z-testiyle karşılaştırılır
  (`proportions_ztest`).
- Farkın güven aralığı için `confint_proportions_2indep(..., method="newcomb")`.
- Küçük sayılarda z-testi sözünü tutmayabilir; Fisher'ın kesin testi
  güvenlidir ama tutucudur.
- Mutlak fark ile göreli artışı karıştırma.
