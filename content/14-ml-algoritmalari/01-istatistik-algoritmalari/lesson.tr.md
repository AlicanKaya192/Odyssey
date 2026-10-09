# İstatistik Algoritmaları

Ortalama, varyans, yüzdelik, korelasyon ve histogram: her veri analizinin ilk
satırları. Formülleri basit görünür, ama bilgisayarda hesaplarken iki tuzak
var: **kayan nokta hatası** ve **sınır durumları**. Bu bölümde her birini
NumPy'nin sonucuyla karşılaştırarak sıfırdan yazıyoruz.

## Varyansı yanlış hesaplamanın kolay yolu

Varyans "kareler ortalaması eksi ortalamanın karesi" diye de yazılabilir:
`E[x²] − (E[x])²`. Tek geçişte hesaplanır, kâğıt üstünde doğrudur. Ama sayılar
büyük ve birbirine yakınsa iki dev sayıyı birbirinden çıkarır ve kayan
noktanın hassasiyeti tükenir.

```python
import numpy as np

rng = np.random.default_rng(1)
x = 1e9 + rng.normal(0, 1, size=100_000)       # bir milyar civarı, sapma 1


def naive_var(values):
    n = len(values)
    s = sum(values)
    s2 = sum(v * v for v in values)
    return s2 / n - (s / n) ** 2               # dev - dev


def two_pass_var(values):
    mean = sum(values) / len(values)
    return sum((v - mean) ** 2 for v in values) / len(values)


print(round(naive_var(x.tolist()), 4), round(two_pass_var(x.tolist()), 4),
      round(float(np.var(x)), 4))
```

```text
256.0 0.9931 0.9931
```

Gerçek varyans yaklaşık 1; tek geçişli formül 256 buldu. `x²` değerleri
10¹⁸ civarında ve `float`'un yaklaşık 16 anlamlı basamağı aradaki küçük farkı
taşıyamıyor (**yıkıcı sadeleşme**, catastrophic cancellation). İki geçişli
yol önce ortalamayı çıkarıp küçük sayılarla çalıştığı için doğru.

## Akan veride varyans: Welford

İki geçiş, verinin iki kez okunabilmesini ister. Veri akıyorsa (sensör,
log) ya da belleğe sığmıyorsa **Welford algoritması** her yeni değerde
ortalamayı ve kare sapmaların toplamını güncelleyerek tek geçişte, sağlam
hesap yapar.

```python
class RunningStats:
    def __init__(self):
        self.n, self.mean, self.m2 = 0, 0.0, 0.0

    def add(self, value):
        self.n += 1
        delta = value - self.mean               # eski ortalamaya uzaklık
        self.mean += delta / self.n
        self.m2 += delta * (value - self.mean)  # eski ve yeni ortalamaya göre

    def var(self):
        return self.m2 / self.n


stats = RunningStats()
for v in x:
    stats.add(float(v))
print(round(stats.mean - 1e9, 6), round(stats.var(), 4))
print(np.isclose(stats.var(), np.var(x)))
```

```text
-0.004581 0.9931
True
```

Tek geçiş, sabit bellek, NumPy ile aynı sonuç. Sinir ağlarındaki batch
normalization katmanının "koşan ortalaması" da benzer bir güncellemeyle
tutulur.

## Yüzdelikler

`q`. yüzdelik, verinin `%q`'sunun altında kaldığı değer. Sıralı listede
konum `(n − 1) · q / 100` tam sayı değilse iki komşu değer arasında
**doğrusal enterpolasyon** yapılır; NumPy'nin varsayılanı budur.

```python
def percentile(values, q):
    s = sorted(values)
    pos = (len(s) - 1) * q / 100
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


data = [7, 1, 3, 9, 4, 6, 2]
for q in (0, 25, 50, 90, 100):
    print(q, round(percentile(data, q), 2), round(float(np.percentile(data, q)), 2))
```

```text
0 1.0 1.0
25 2.5 2.5
50 4.0 4.0
90 7.8 7.8
100 9.0 9.0
```

Medyan (50. yüzdelik) 4; 90. yüzdelik iki değerin arasında, 7,8. Yüzdelik
tanımı tek değil: NumPy'de `method` ile başka yöntemler de seçilebilir;
küçük veride sonuçlar ayrışır.

## Korelasyon

Pearson korelasyonu iki değişkenin **doğrusal** ilişkisini −1 ile 1 arasında
ölçer: ortalamadan sapmaların nokta çarpımı, iki sapma vektörünün boylarının
çarpımına bölünür.

```python
def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    da, db = a - a.mean(), b - b.mean()
    return (da @ db) / np.sqrt((da @ da) * (db @ db))


hours = rng.uniform(0, 10, 50)
score = 40 + 5 * hours + rng.normal(0, 8, 50)
print(round(pearson(hours, score), 4), round(np.corrcoef(hours, score)[0, 1], 4))
xs = np.linspace(-3, 3, 61)
print(round(pearson(xs, xs ** 2), 4))
```

```text
0.8329 0.8329
0.0
```

Çalışma saati ile not arasında güçlü bir doğrusal ilişki: 0,83. Ama ikinci
satır önemli: `y = x²` kusursuz bir ilişki olduğu hâlde korelasyon **0**.
Korelasyon yalnızca doğrusal ilişkiyi görür; "korelasyon yok" "ilişki yok"
demek değildir.

<figure class="fig">
<svg viewBox="0 0 360 240" width="360" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="30" y1="218" x2="330" y2="218"/><line class="grid" x1="180" y1="10" x2="180" y2="225"/><polyline class="curve" points="30.0,20.0 35.0,33.0 40.0,45.5 45.0,57.6 50.0,69.3 55.0,80.5 60.0,91.3 65.0,101.6 70.0,111.5 75.0,121.0 80.0,130.0 85.0,138.6 90.0,146.7 95.0,154.4 100.0,161.7 105.0,168.5 110.0,174.9 115.0,180.8 120.0,186.3 125.0,191.4 130.0,196.0 135.0,200.2 140.0,203.9 145.0,207.2 150.0,210.1 155.0,212.5 160.0,214.5 165.0,216.0 170.0,217.1 175.0,217.8 180.0,218.0 185.0,217.8 190.0,217.1 195.0,216.0 200.0,214.5 205.0,212.5 210.0,210.1 215.0,207.2 220.0,203.9 225.0,200.2 230.0,196.0 235.0,191.4 240.0,186.3 245.0,180.8 250.0,174.9 255.0,168.5 260.0,161.7 265.0,154.4 270.0,146.7 275.0,138.6 280.0,130.0 285.0,121.0 290.0,111.5 295.0,101.6 300.0,91.3 305.0,80.5 310.0,69.3 315.0,57.6 320.0,45.5 325.0,33.0 330.0,20.0" fill="none"/><line class="curve3" x1="30" y1="166.7" x2="330" y2="166.7"/><text class="dim" x="334" y="222" font-size="12">x</text><text class="dim" x="186" y="18" font-size="12">y = x²</text></svg>
<figcaption>y = x²: kusursuz bir ilişki. Ama en uygun doğru (kesik) yatay; sol yarıdaki düşüş sağ yarıdaki yükselişi götürüyor ve Pearson korelasyonu 0 çıkıyor.</figcaption>
</figure>

## Histogram

Histogram değer aralığını eşit genişlikte kutulara böler ve her kutuya düşen
değeri sayar. İki sınır durumu var: aralığın dışındakiler sayılmaz, tam üst
sınıra eşit değer son kutuya girer.

```python
def histogram(values, bins, low, high):
    counts = [0] * bins
    width = (high - low) / bins
    for v in values:
        if v < low or v > high:
            continue                           # aralık dışı
        i = min(int((v - low) / width), bins - 1)   # üst sınır: son kutu
        counts[i] += 1
    return counts


vals = rng.normal(0, 1, 1000)
print(histogram(vals, 6, -3, 3))
print(np.histogram(vals, bins=6, range=(-3, 3))[0].tolist())
```

```text
[19, 127, 333, 333, 152, 30]
[19, 127, 333, 333, 152, 30]
```

Aynı sayılar. Normal dağılımdan bin değerin üçte ikisi kadarı ortadaki iki
kutuda (−1 ile 1 arası).

## Özet

- `E[x²] − (E[x])²` büyük ve yakın sayılarda yıkıcı sadeleşmeyle bozulur;
  önce ortalamayı çıkar ya da Welford kullan.
- Welford: tek geçiş, sabit bellek, sağlam varyans.
- Yüzdelik: sıralı listede konum `(n − 1) · q / 100`, arada doğrusal
  enterpolasyon.
- Pearson korelasyonu yalnızca doğrusal ilişkiyi ölçer; `x²` ile 0.
- Histogramda aralık dışı ve üst sınır, iki sınır durumu.
