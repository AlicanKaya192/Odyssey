# Karar ve Raporlama

Bir test hiçbir zaman "p < 0,05, yayınla" kadar basit bitmez. Karar,
etkinin **ne kadar** olduğuna, bu belirsizliğin **ne kadar** olduğuna ve
yanlış kararın **neye mal olacağına** bağlıdır. Bu bölüm, güven aralığını
önceden yazılmış bir eşikle okumayı, "belirsiz" bir sonuçla ne
yapılacağını ve kararı herkesin aynı biçimde anlayacağı bir rapora
dökmeyi gösteriyor.

## Dört sonuç

İlk A/B Testinin Çözümlemesi bölümündeki gibi bir **pratik eşik** var:
B'nin satın almayı en az 0,3 puan artırması gerekiyor (altındaki bir artış
değişikliğin maliyetini karşılamıyor). Güven aralığı bu eşiğe ve sıfıra
göre dört yere düşebilir. Dört farklı testle görelim:

```python
import numpy as np
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment

THRESHOLD = 0.003


def interval(test):
    k = test.groupby("group")["bought"].sum()
    n = test.groupby("group").size()
    return confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])


def verdict(low, high, threshold=THRESHOLD):
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"


cases = {"win": (30000, 0.15, 141), "loss": (30000, -0.15, 142),
         "small": (4000, 0.12, 143), "tiny": (1500000, 0.01, 144)}
for name, (n, lift, seed) in cases.items():
    low, high = interval(make_experiment(n=n, seed=seed, lift=lift))
    print(name, round(low * 100, 2), round(high * 100, 2), verdict(low, high))
```

```text
win 1.01 2.53 ship
loss -2.95 -1.54 harm
small -1.31 2.78 inconclusive
tiny 0.03 0.24 not worth it
```

Sayılar puan cinsinden (%95 aralığın iki ucu):

| Sonuç | Aralık | Karar |
|---|---|---|
| `win` | tamamen eşiğin üstünde | uygula |
| `loss` | tamamen sıfırın altında | uygulama: zararlı |
| `small` | sıfırı da eşiği de içine alıyor | belirsiz: veri yetmedi |
| `tiny` | sıfırın üstünde ama tamamen eşiğin altında | etki gerçek ama değmez |

Son satır önemli: 1,5 milyon kullanıcılık `tiny` testi **anlamlı** bir fark
buluyor, ama aralığın üst ucu bile eşiğin altında. "İstatistiksel olarak
anlamlı" ile "uygulamaya değer" aynı şey değildir; Etki Büyüklüğü
bölümündeki ayrım burada karara dönüşüyor.

## Belirsiz sonuçla ne yapılır?

`small` testi 4000 kişiyle yapılmış; aralık -1,31 ile 2,78 puan arasında.
Bu "B işe yaramıyor" demek değil, "bilmiyoruz" demek. Üç yol var:

1. **Daha çok veri:** Örneklem Büyüklüğü bölümündeki hesapla testi uzatmak
   (önceden planlanmışsa).
2. **Aralığın söylediğini raporlamak:** "artışın üst sınırı 2,78
   puan" demek bile bir bilgidir.
3. **Riski sormak:** B'yi seçersek ve yanılırsak ne kaybederiz? Bayesçi
   Bakışa Giriş bölümündeki Beta dağılımlarıyla:

```python
small = make_experiment(n=4000, seed=143, lift=0.12)
k = small.groupby("group")["bought"].sum()
n = small.groupby("group").size()
rng = np.random.default_rng(1401)
pa = rng.beta(1 + k["A"], 1 + n["A"] - k["A"], 200000)
pb = rng.beta(1 + k["B"], 1 + n["B"] - k["B"], 200000)
print(round(float((pb > pa).mean()), 3))
print(round(float(np.maximum(pa - pb, 0).mean() * 100), 3))
```

```text
0.76
0.146
```

B'nin daha iyi olma olasılığı 0,76. İkinci sayı **beklenen
kayıp**: B'yi seçtiğimizde, yanıldığımız durumlarda kaybedeceğimiz farkın
ortalaması (0,146 puan). Değişiklik ucuz ve geri alınabilirse
küçük bir beklenen kayıp kabul edilebilir; pahalı ve kalıcıysa daha çok
veri beklenir. Bu eşik de, pratik eşik gibi, test başlamadan yazılır.

## Etkiyi paraya çevirmek

Karar verenler çoğu zaman puan değil para sorar. Etkiyi tek bir sayı olarak
değil, aralık olarak çevirin. Yılda 2 milyon ziyaretçi ve ortalama 100 TL
sepet için `win` testi:

```python
visitors, basket = 2_000_000, 100
low, high = interval(make_experiment(n=30000, seed=141, lift=0.15))
print(round(low * visitors * basket), round(high * visitors * basket))
```

```text
2023143 5053874
```

Yıllık ek satış 2 023 143 ile 5 053 874 TL arasında. Tek bir
sayı yazmak, aralığın genişliğini gizler; Yenilik
Etkisi ve Uzun Vadeli Etki bölümündeki gibi kısa testin etkisi zamanla
küçülebilir.

## Rapor

İyi bir test raporu bir sayfayı geçmez ve her zaman aynı sırayı izler:

1. **Soru ve karar kuralı:** neyi, hangi metrikle, hangi eşikle (testten
   önce yazılmış hâliyle).
2. **Güven denetimleri:** SRM, A/A, denge.
3. **Birincil metrik:** iki oran, fark, güven aralığı, p.
4. **Koruma ve ikincil metrikler:** bozulma var mı; ikinciller karar vermez.
5. **Karar:** dört sonuçtan hangisi ve neden.
6. **Sınırlar:** süre, yenilik etkisi, segmentler, karışma riski.

## Özet

- Karar, güven aralığının sıfıra ve önceden yazılmış pratik eşiğe göre yeri
  ile verilir: uygula, zararlı, belirsiz, değmez.
- Anlamlı olmak uygulamaya değer olmak değildir.
- Belirsiz sonuç "etki yok" demek değildir; daha çok veri, aralığı
  raporlamak ya da beklenen kaybı tartmak gerekir.
- Para karşılığı aralık olarak yazılır.
- Rapor her zaman aynı sırayla, kısa ve önceden yazılmış kurallara bağlı.
