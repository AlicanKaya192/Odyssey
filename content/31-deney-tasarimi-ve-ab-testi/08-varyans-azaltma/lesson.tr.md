# Varyans Azaltma: CUPED

Örneklem Büyüklüğü bölümünde gereken kullanıcı sayısının metriğin
varyansıyla doğru orantılı olduğunu gördük. Gürültülü bir metrikte küçük
bir etkiyi yakalamak için ya çok kullanıcı ya çok zaman gerekir. Bu bölüm
üçüncü bir yol gösteriyor: gürültünün bir kısmını, deneyden **önce**
toplanmış veriyle açıklayıp çıkarmak. Yöntemin adı **CUPED** (Controlled
experiment Using Pre-Experiment Data).

## Gürültünün kaynağı: kullanıcılar birbirinden farklı

Bir uygulamada geçirilen dakikaları ölçen bir testimiz var. B, dakikaları
gerçekte %3 artırıyor. Ama kullanıcılar zaten çok farklı: kimi günde iki
dakika, kimi bir saat kalıyor. Bu fark B'den gelmiyor, kişinin kendisinden
geliyor ve ortalamaların farkını gürültüye boğuyor.

```python
import numpy as np
from scipy import stats
from ab_data import make_engagement_test

test = make_engagement_test()
is_b = (test["group"] == "B").to_numpy()
minutes = test["minutes"].to_numpy()


def compare(y, b):
    diff = y[b].mean() - y[~b].mean()
    se = np.sqrt(y[b].var(ddof=1) / b.sum() + y[~b].var(ddof=1) / (~b).sum())
    p = 2 * stats.norm.sf(abs(diff / se))
    return round(float(diff), 3), round(float(se), 3), round(float(p), 4)


print(compare(minutes, is_b))
```

```text
(1.134, 0.355, 0.0014)
```

Fark 1,13 dakika, standart hatası 0,355. Test anlamlı
çıkıyor ama aralık geniş.

## Fikir: deneyden önceki davranış

Aynı kullanıcıların testten önceki iki haftadaki dakikalarını
(`pre_minutes`) biliyoruz. Bir saat kalan kişi testten önce de çok
kalıyordu. Bu bilgiyle her kullanıcının dakikasını düzeltelim:

$$Y_{\text{cuped}} = Y - \theta\,(X - \bar{X}), \qquad \theta = \frac{\operatorname{cov}(X, Y)}{\operatorname{var}(X)}$$

Burada X deneyden önceki değer. θ, X'in Y'yi ne kadar açıkladığıdır
(doğrusal regresyonun eğimi). X atamadan **önce** ölçüldüğü için iki
grupta ortalaması aynıdır; düzeltme farkı değiştirmez, yalnızca
gürültüyü azaltır.

```python
pre = test["pre_minutes"].to_numpy()


def cuped(y, x):
    theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
    return y - theta * (x - x.mean())


rho = np.corrcoef(pre, minutes)[0, 1]
adjusted = cuped(minutes, pre)
print(round(rho, 3), round(adjusted.var() / minutes.var(), 3))
print(compare(adjusted, is_b))
```

```text
0.75 0.437
(1.04, 0.235, 0.0)
```

Önceki ve sonraki dakikaların korelasyonu 0,75. Düzeltmeden
sonra varyansın yalnızca %44 kadarı kalıyor; bu, 1 − ρ²
formülünün verdiği değerle aynı. Fark neredeyse yerinde duruyor
(1,04 dakika), standart hata ise 0,235 oluyor ve p
değeri çok daha küçük. Gereken kullanıcı sayısı varyansla orantılı
olduğundan, CUPED'li bir test aynı gücü kullanıcıların yaklaşık
%44 kadarıyla verir.

## Benzetimle: güç artıyor, yanlış alarm artmıyor

Tek bir deneye bakıp karar vermeyelim. 300 gerçek (%3 etkili) ve 300 A/A
deneyinde iki yöntemi karşılaştıralım:

```python
power = np.zeros(2)
alarm = np.zeros(2)
for s in range(300):
    for lift, counter in [(0.03, power), (0.0, alarm)]:
        t = make_engagement_test(seed=2000 + s, lift=lift)
        b = (t["group"] == "B").to_numpy()
        y = t["minutes"].to_numpy()
        x = t["pre_minutes"].to_numpy()
        counter += [compare(y, b)[2] < 0.05, compare(cuped(y, x), b)[2] < 0.05]
print(np.round(power / 300, 3), np.round(alarm / 300, 3))
```

```text
[0.613 0.92 ] [0.05 0.06]
```

Düz karşılaştırmanın gücü %61,3, CUPED'inki %92,0. A/A deneylerinde iki
yöntem de %5 civarında yanlış alarm veriyor (%5,0 ve
%6,0). CUPED hileli bir kestirme değil: testin geçerliliğini
bozmadan gürültüyü azaltıyor.

## Tuzak: deney sırasında ölçülen ortak değişken

Düzeltmenin farkı değiştirmemesinin tek şartı X'in **B'den
etkilenmemesi**. Aynı formülü test sırasındaki oturum sayısıyla
(`sessions`) uygulayalım. Oturumlar dakikalarla birlikte artıyor, yani B
onları da artırıyor:

```python
sessions = test["sessions"].to_numpy()
print(compare(cuped(minutes, sessions), is_b))
```

```text
(0.403, 0.184, 0.0286)
```

Fark 0,40 dakikaya iniyor: gerçek etkinin yaklaşık yarısı
(0,82 dakika) kayboldu. Düzeltme, B'nin oturumları artırarak
yaptığı etkiyi "oturum farkı" diye çıkarıp attı. **Ortak değişken
deneyden önce ölçülür;** test sırasında ölçülen hiçbir şey kullanılmaz.

## Özet

- CUPED, deneyden önceki değerle (X) her kullanıcının metriğini düzeltir:
  Y − θ(X − X̄).
- Kalan varyans yaklaşık 1 − ρ²; ρ yüksekse kazanç büyüktür.
- Etkinin tahmini değişmez, standart hata küçülür, güç artar, yanlış
  alarm %5'te kalır.
- X, atamadan önce ölçülmüş olmalı; testten etkilenen bir değişken
  etkiyi silebilir.
