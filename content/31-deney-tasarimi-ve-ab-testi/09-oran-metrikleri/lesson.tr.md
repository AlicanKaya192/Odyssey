# Oran Metrikleri ve Delta Yöntemi

Bazı metrikler iki toplamın oranıdır: tıklama oranı (tıklama / gösterim),
sipariş başına gelir (gelir / sipariş), oturum başına süre. Bu metriklerde
sinsi bir tuzak var: deneyde **atanan** şey kullanıcıdır, ama oranın
paydası kullanıcı değil gösterimdir. Bu bölüm, bu farkı unutan testin
neden fazla alarm verdiğini ölçüyor ve doğru standart hatayı veren
**delta yöntemini** gösteriyor.

## Kullanıcı başına çok gösterim

Bir sayfa tasarımı testinde her kullanıcı birkaç sayfa görüyor ve bazılarına
tıklıyor. Metrik, tıklama oranı (CTR): toplam tıklama / toplam gösterim.
Bu veride B'nin hiçbir etkisi yok (A/A).

```python
import numpy as np
from scipy import stats
from ab_data import make_pageviews

views = make_pageviews()
sums = views.groupby("group")[["pageviews", "clicks"]].sum()
print(sums)
print(round(views["pageviews"].mean(), 2))
```

```text
       pageviews  clicks
group                   
A          25368    1676
B          24035    1572
8.23
```

Her grupta yaklaşık 3000 kullanıcı ama 25 368 ve 24 035
gösterim var; kullanıcı başına ortalama 8,23 gösterim.

## Saf test: her gösterimi bağımsız saymak

Oranları Karşılaştırmak bölümündeki iki oran z-testi her denemeyi
bağımsız sayar. Gösterimleri deneme diye verirsek:

```python
def naive_test(table):
    s = table.groupby("group")[["pageviews", "clicks"]].sum()
    r = s["clicks"] / s["pageviews"]
    se = np.sqrt((r * (1 - r) / s["pageviews"]).sum())
    z = (r["B"] - r["A"]) / se
    return round(float(se), 5), round(float(2 * stats.norm.sf(abs(z))), 4)


print(naive_test(views))
```

```text
(0.00223, 0.7663)
```

Ama aynı kullanıcının gösterimleri bağımsız değil: bazı kullanıcılar
neredeyse her şeye tıklar, bazıları hiç tıklamaz. Bir kullanıcının on
gösterimi on ayrı kişi gibi sayılınca örneklem olduğundan büyük görünür ve
standart hata olduğundan küçük çıkar.

## Delta yöntemi

Doğru birim kullanıcıdır. Her kullanıcının tıklaması Y, gösterimi X olsun;
oran R = Ȳ / X̄ (ortalamaların oranı, yani toplamların oranı). İki
ortalamanın oranı için **delta yöntemi** şu varyansı verir:

$$\operatorname{var}(R) \approx \frac{1}{n\,\bar{X}^2}\left(s_Y^2 - 2R\,s_{XY} + R^2 s_X^2\right)$$

Burada n kullanıcı sayısı, s² varyanslar ve s_XY kovaryans; hepsi
**kullanıcı düzeyinde** hesaplanır.

```python
def delta_test(table):
    parts = {}
    for g in ["A", "B"]:
        t = table[table["group"] == g]
        x = t["pageviews"].to_numpy(dtype=float)
        y = t["clicks"].to_numpy(dtype=float)
        r = y.mean() / x.mean()
        cov = np.cov(x, y)[0, 1]
        var = (y.var(ddof=1) - 2 * r * cov + r ** 2 * x.var(ddof=1))
        parts[g] = (r, var / (len(x) * x.mean() ** 2))
    se = np.sqrt(parts["A"][1] + parts["B"][1])
    z = (parts["B"][0] - parts["A"][0]) / se
    return round(float(se), 5), round(float(2 * stats.norm.sf(abs(z))), 4)


print(delta_test(views))
```

```text
(0.00278, 0.8116)
```

Delta yönteminin standart hatası saf testinkinin 1,25 katı.
Bu örnekte iki test de "fark yok" diyor; peki fark ne zaman önemli olur?

## Benzetimle: saf test fazla alarm veriyor

400 A/A deneyinde iki testin yanlış alarm oranını sayalım:

```python
alarms = np.zeros(2)
for s in range(400):
    t = make_pageviews(seed=6000 + s)
    alarms += [naive_test(t)[1] < 0.05, delta_test(t)[1] < 0.05]
print(np.round(alarms / 400, 3))
```

```text
[0.132 0.06 ]
```

Saf test hiçbir şeyin değişmediği deneylerin %13,2 kadarında
"anlamlı" diyor: söz verilen %5'in çok üstünde. Delta yöntemi
%6,0 ile %5 civarında kalıyor.

## Bootstrap ile sağlamak

Bootstrap ve Permütasyon Testi bölümünde gördüğümüz gibi yeniden örnekleme
**atama biriminde** yapılır. Kullanıcıları (tıklamaları ve gösterimleriyle
birlikte) yeniden örnekleyip A grubunun oranının ne kadar oynadığına
bakalım:

```python
a = views[views["group"] == "A"]
x = a["pageviews"].to_numpy()
y = a["clicks"].to_numpy()
rng = np.random.default_rng(901)
ratios = []
for _ in range(2000):
    i = rng.integers(0, len(x), len(x))
    ratios.append(y[i].sum() / x[i].sum())
r = y.sum() / x.sum()
delta_se = np.sqrt((y.var(ddof=1) - 2 * r * np.cov(x, y)[0, 1]
                    + r ** 2 * x.var(ddof=1)) / (len(x) * x.mean() ** 2))
print(round(float(np.std(ratios)), 5), round(float(delta_se), 5))
```

```text
0.00199 0.00202
```

Kullanıcı düzeyindeki bootstrap ile delta yöntemi aynı standart hatayı
veriyor. Delta yöntemi, bootstrap'in binlerce tekrarla bulduğunu tek
formülle buluyor; bu yüzden büyük deney platformlarında yaygın.

## İki farklı "ortalama oran"

Oran metriği iki biçimde tanımlanabilir ve ikisi farklı sorular sorar:

- **Toplamların oranı** (Σ tıklama / Σ gösterim): her gösterim eşit
  ağırlıkta; çok gösterimli kullanıcı oranı daha çok etkiler. Delta
  yöntemi gerekir.
- **Kullanıcı oranlarının ortalaması** (her kullanıcının tıklama /
  gösterim oranının ortalaması): her kullanıcı eşit ağırlıkta. Bu zaten
  kullanıcı düzeyinde bir metrik; sıradan Welch testi yeter.

Hangisinin raporlanacağı Deney Sorusu ve Metrik Seçimi bölümündeki gibi
önceden yazılır.

## Özet

- Atama birimi (kullanıcı) ile metriğin paydası (gösterim) farklıysa
  gösterimler bağımsız değildir.
- Gösterimleri bağımsız sayan test standart hatayı küçük bulur ve fazla
  alarm verir.
- Delta yöntemi oranın varyansını kullanıcı düzeyindeki varyans ve
  kovaryanslardan hesaplar.
- Kullanıcı düzeyinde bootstrap aynı sonucu verir.
