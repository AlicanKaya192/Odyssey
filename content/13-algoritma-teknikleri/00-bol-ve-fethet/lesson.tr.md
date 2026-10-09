# Böl ve Fethet

Temel Algoritmalar modülünde merge sort ve quick sort'u yazdın: listeyi ikiye böl, iki yarıyı
kendinle çöz, sonuçları birleştir. Bu bölümde aynı fikri bir **teknik**
olarak ele alıyoruz: bir böl-fethet algoritmasının maliyeti nasıl
hesaplanır, ne zaman işe yarar, ne zaman yaramaz ve sıralamanın dışında
nerede kullanılır.

<figure class="fig">
  <div class="flow">
    <span class="node">Böl<br><small>küçük parçalar</small></span><span class="arrow">→</span>
    <span class="node acc">Fethet<br><small>her parçayı kendinle çöz</small></span><span class="arrow">→</span>
    <span class="node ok">Birleştir<br><small>cevapları topla</small></span>
  </div>
  <figcaption>Parça yeterince küçükse (temel durum) doğrudan çözülür; değilse aynı üç adım parçanın içinde tekrar eder.</figcaption>
</figure>

## Maliyeti hesaplamak: özyineleme ağacı

Bir böl-fethet algoritmasının maliyeti üç sayıya bağlı: problem **kaç
parçaya** bölünüyor, parçalar **ne kadar küçük** ve bölme + birleştirme
**ne kadar iş** tutuyor. Bunu bir ağaç gibi çizmek işi kolaylaştırır. Merge
sort'ta her düğüm kendi parçasının boyu kadar iş yapıyor (birleştirme):

<figure class="fig">
<svg viewBox="0 0 573 180" width="573" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="30" font-size="12">seviye 0: toplam n</text>
<text class="dim" x="4" y="94" font-size="12">seviye 1: toplam n</text>
<text class="dim" x="4" y="158" font-size="12">seviye 2: toplam n</text>
<line class="line" x1="212.8" y1="89.0" x2="150.8" y2="153.0"/>
<line class="line" x1="212.8" y1="89.0" x2="274.8" y2="153.0"/>
<line class="line" x1="460.8" y1="89.0" x2="398.8" y2="153.0"/>
<line class="line" x1="460.8" y1="89.0" x2="522.8" y2="153.0"/>
<line class="line" x1="336.8" y1="25.0" x2="212.8" y2="89.0"/>
<line class="line" x1="336.8" y1="25.0" x2="460.8" y2="89.0"/>
<rect class="box" x="130.0" y="136.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="150.8" y="157.9" font-size="14" text-anchor="middle">n/4</text>
<rect class="box" x="192.0" y="72.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="212.8" y="93.9" font-size="14" text-anchor="middle">n/2</text>
<rect class="box" x="254.0" y="136.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="274.8" y="157.9" font-size="14" text-anchor="middle">n/4</text>
<circle class="box" cx="336.8" cy="25.0" r="17"/>
<text class="ink" x="336.8" y="29.9" font-size="14" text-anchor="middle">n</text>
<rect class="box" x="378.0" y="136.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="398.8" y="157.9" font-size="14" text-anchor="middle">n/4</text>
<rect class="box" x="440.0" y="72.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="460.8" y="93.9" font-size="14" text-anchor="middle">n/2</text>
<rect class="box" x="502.0" y="136.0" width="41.5" height="34" rx="8"/>
<text class="ink" x="522.8" y="157.9" font-size="14" text-anchor="middle">n/4</text>
</svg>
<figcaption>Merge sort'un özyineleme ağacı. Her düğüm kendi parçasının boyu kadar iş yapar; her seviyenin toplamı n, seviye sayısı log₂ n.</figcaption>
</figure>

Her seviyedeki parçaların toplam boyu yine `n`, yani her seviye `n` iş
tutuyor. Seviye sayısı `log₂ n` (her seviyede parçalar yarıya iniyor).
Toplam: `n log n`.

Farklı şekilleri ölçelim. Aşağıdaki fonksiyonlar bir şey hesaplamıyor,
yalnızca dört farklı böl-fethet düzeninin **ne kadar iş** yaptığını
sayıyor:

```python
def work_a(n):          # 2 parça, birleştirme n   (merge sort)
    if n <= 1:
        return 1
    return work_a(n // 2) + work_a(n - n // 2) + n

def work_b(n):          # 1 parça, birleştirme n
    if n <= 1:
        return 1
    return work_b(n // 2) + n

def work_c(n):          # 1 parça, birleştirme 1      (ikili arama)
    if n <= 1:
        return 1
    return work_c(n // 2) + 1

def work_d(n):          # 2 parça, birleştirme 1
    if n <= 1:
        return 1
    return work_d(n // 2) + work_d(n - n // 2) + 1

for n in [1024, 1_048_576]:
    print(n, work_a(n), work_b(n), work_c(n), work_d(n))
```

```text
1024 11264 2047 11 2047
1048576 22020096 2097151 21 2097151
```

`n` bin kat büyüyünce (1024 → 1 048 576):

- **`work_a`** (merge sort) yaklaşık iki bin kat büyüdü: her seviye
  `n`, seviye sayısı `log n` → `O(n log n)`.
- **`work_b`** yaklaşık bin kat büyüdü: en üst seviye `n`, altındaki `n/2`,
  sonra `n/4`… toplam `2n`'den az. İşin çoğu **tepede** → `O(n)`.
- **`work_c`** (ikili arama) yalnızca 10 arttı: `O(log n)`.
- **`work_d`** bin kat büyüdü: her düğüm 1 iş ama düğüm sayısı `2n` civarı.
  İşin çoğu **yapraklarda** → `O(n)`.

Kısaca: her seviyede iş aynıysa `iş × log n`; yukarıdan aşağı azalıyorsa
tepe kazanır; aşağı doğru artıyorsa yapraklar kazanır. Ders kitaplarında bu
kurala **ana teorem (master theorem)** denir; ağacı çizip seviyeleri
toplamak çoğu zaman aynı sonucu verir.

## En büyük toplamlı alt dizi

Bir hisse senedinin günlük kâr/zararı elinde: `[2, -5, 6, -2, 3, -8, 4]`.
**Art arda günlerden** oluşan hangi dönemde toplam kâr en büyük? Kaba
kuvvet bütün başlangıç–bitiş çiftlerini dener: `O(n²)`.

Böl ve fethet ile: en iyi dönem ya **tamamen sol yarıda**, ya **tamamen sağ
yarıda** ya da **ortadan geçiyor**. İlk ikisini özyineleme çözer. Ortadan
geçeni bulmak kolay: ortadan sola doğru en iyi toplam + ortadan sağa doğru
en iyi toplam.

```python
def max_sub(values, lo, hi):
    if lo == hi:                        # tek eleman
        return values[lo]
    mid = (lo + hi) // 2
    left = max_sub(values, lo, mid)
    right = max_sub(values, mid + 1, hi)
    total, best_left = 0, values[mid]
    for i in range(mid, lo - 1, -1):    # ortadan sola
        total += values[i]
        best_left = max(best_left, total)
    total, best_right = 0, values[mid + 1]
    for i in range(mid + 1, hi + 1):    # ortadan sağa
        total += values[i]
        best_right = max(best_right, total)
    return max(left, right, best_left + best_right)

values = [2, -5, 6, -2, 3, -8, 4]
print(max_sub(values, 0, len(values) - 1))
```

```text
7
```

En iyi dönem `6, -2, 3`: toplam 7. Her seviyede ortadan geçen kısım
toplam `n` adım, seviye sayısı `log n`: `O(n log n)`. 2000 günlük rastgele
veride toplama adımlarını saydık:

```text
brute force       : 2001000 steps, answer 1115
divide and conquer: 21952 steps, answer 1115
```

Aynı cevap, doksan kattan fazla daha az adım. Bu problemin `O(n)` çözümü de
var (Kadane algoritması); onu Dinamik Programlama bölümünde göreceğiz.

## Büyük sayıları çarpmak: Karatsuba

Okulda öğrendiğin çarpma yönteminde iki `n` basamaklı sayının her
basamağı öbürünün her basamağıyla çarpılır: `n²` tane tek basamak
çarpımı. Böl ve fethet ile sayıları ikiye bölelim:

`x = a·10ʰ + b`, `y = c·10ʰ + d` → `x·y = ac·10²ʰ + (ad + bc)·10ʰ + bd`

Dört yarım boy çarpım (`ac`, `ad`, `bc`, `bd`): hâlâ `n²`. **Karatsuba**'nın
1960'taki fikri: ortadaki terim için iki çarpım yerine bir tane yeter,

`ad + bc = (a + b)(c + d) − ac − bd`

ve `ac` ile `bd` zaten hesaplanmıştı. Dört yerine **üç** çarpım:

```python
def karatsuba(x, y):
    if x < 10 or y < 10:                     # tek basamak: doğrudan
        return x * y
    half = max(len(str(x)), len(str(y))) // 2
    a, b = divmod(x, 10 ** half)
    c, d = divmod(y, 10 ** half)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    middle = karatsuba(a + b, c + d) - ac - bd
    return ac * 10 ** (2 * half) + middle * 10 ** half + bd

print(karatsuba(1234, 5678), 1234 * 5678)
```

```text
7006652 7006652
```

Rastgele sayılarda tek basamak çarpımlarını saydık (okul yöntemi de aynı
bölmeyle, dört çarpımla):

```text
  8 digits: school     52, karatsuba     39
 64 digits: school   3634, karatsuba   1083
512 digits: school 228676, karatsuba  28375
```

Fark basamak sayısı büyüdükçe açılıyor: üç parçaya bölünen ağaçta yaprak
sayısı `3^(log₂ n) = n^1,58`, dörtte `n²`. CPython büyük tam sayıları
çarparken bu yöntemi kullanır; Python'da `2 ** 100000` gibi devasa sayıları
hızla çarpabilmen biraz da bundan.

## En yakın nokta çifti

Düzlemde binlerce nokta var (dükkânlar, sensörler, müşteriler); birbirine
**en yakın iki nokta** hangisi? Kaba kuvvet her çifte bakar: `n(n−1)/2`
uzaklık.

Böl ve fethet:

1. Noktaları `x`'e göre sırala, ortadan dikey bir çizgiyle ikiye böl.
2. İki yarıda en yakın çifti özyinelemeyle bul; küçük olanı `d`.
3. Çizgiyi kesen bir çift `d`'den yakın olabilir, ama o iki nokta da
   çizgiye `d`'den yakın olmak zorunda. Yalnızca bu **şeritteki** noktalara
   bak; şeridi `y`'ye göre sırala, her nokta yalnızca `y` farkı `d`'den küçük
   komşularıyla karşılaştırılır.

<figure class="fig">
<svg viewBox="0 0 420 250" width="420" xmlns="http://www.w3.org/2000/svg">
<rect class="box" x="168" y="8" width="84" height="230" fill-opacity=".35"/>
<line class="curve3" x1="168" y1="8" x2="168" y2="238" stroke-dasharray="5 4"/>
<line class="curve3" x1="252" y1="8" x2="252" y2="238" stroke-dasharray="5 4"/>
<line class="curve" x1="210" y1="4" x2="210" y2="242"/>
<circle class="dot" cx="109.7" cy="40.6" r="5"/>
<circle class="dot2" cx="170.5" cy="51.0" r="5"/>
<circle class="dot" cx="45.3" cy="100.3" r="5"/>
<circle class="dot" cx="368.8" cy="180.1" r="5"/>
<circle class="dot" cx="310.8" cy="64.4" r="5"/>
<circle class="dot2" cx="223.9" cy="75.3" r="5"/>
<circle class="dot" cx="85.6" cy="41.2" r="5"/>
<circle class="dot" cx="101.5" cy="205.5" r="5"/>
<circle class="dot" cx="335.0" cy="181.3" r="5"/>
<circle class="dot" cx="324.2" cy="58.7" r="5"/>
<circle class="dot" cx="137.7" cy="145.4" r="5"/>
<circle class="dot" cx="298.1" cy="190.9" r="5"/>
<circle class="dot" cx="354.4" cy="37.3" r="5"/>
<circle class="dot2" cx="250.2" cy="154.3" r="5"/>
<circle class="dot2" cx="212.3" cy="55.6" r="5"/>
<circle class="dot2" cx="200.0" cy="37.9" r="5"/>
<circle class="dot" cx="375.1" cy="193.1" r="5"/>
<circle class="dot2" cx="228.1" cy="80.0" r="5"/>
<circle class="dot" cx="365.4" cy="134.5" r="5"/>
<circle class="dot" cx="355.3" cy="189.6" r="5"/>
<circle class="dot2" cx="213.2" cy="102.8" r="5"/>
<circle class="dot2" cx="247.6" cy="106.2" r="5"/>
<text class="dim" x="172" y="236" font-size="12">d</text>
<text class="dim" x="240" y="236" font-size="12">d</text>
</svg>
<figcaption>Mor çizgi ikiye böler. Çizgiyi kesen yakın bir çift ancak kesik çizgilerin arasındaki şeritte olabilir: yalnızca turuncu noktalar karşılaştırılır.</figcaption>
</figure>

```python
import math

def closest(points):                     # points x'e göre sıralı
    n = len(points)
    if n <= 3:
        return min((math.dist(p, q) for i, p in enumerate(points)
                    for q in points[i + 1:]), default=math.inf)
    mid = n // 2
    mid_x = points[mid][0]
    d = min(closest(points[:mid]), closest(points[mid:]))
    strip = sorted((p for p in points if abs(p[0] - mid_x) < d),
                   key=lambda p: p[1])
    for i, p in enumerate(strip):
        for q in strip[i + 1:]:
            if q[1] - p[1] >= d:         # yukarıdakiler daha da uzak
                break
            d = min(d, math.dist(p, q))
    return d
```

2000 rastgele noktada iki yöntemin hesapladığı uzaklık sayısı:

```text
brute force       : 1999000 distances, closest 0.1504
divide and conquer: 2271 distances, closest 0.1504
```

Aynı cevap, kaba kuvvetin yaklaşık binde biri kadar uzaklık hesabıyla. Şeritte her
noktanın en fazla birkaç komşusuna bakıldığı ispatlanabiliyor; toplam
`O(n log n)`. Temel Algoritmalar modülündeki k-d ağacı da aynı fikirle çalışır: uzayı ikiye böl,
uzak yarıyı ele.

## Ne zaman işe yaramaz?

- **Parçalar örtüşüyorsa.** `fib(n) = fib(n−1) + fib(n−2)` iki parçaya
  bölüyor ama parçalar aynı alt problemleri tekrar tekrar çözüyor; üstel
  büyüyor. Bunun çaresi böl-fethet değil, **dinamik programlama**: her alt
  problemi bir kez çöz, sakla.
- **Birleştirme pahalıysa.** Birleştirme `O(n²)` tutuyorsa bölmenin
  kazancı kaybolur.
- **Problem küçülmüyorsa.** Parçalar gerçekten daha küçük olmalı; quick
  sort'un kötü pivotunda bir parça hep `n − 1` kalıyordu.

## Özet

- Böl ve fethet: böl, parçaları kendinle çöz, birleştir.
- Maliyet özyineleme ağacından: seviyelerdeki işleri topla. Her seviye aynıysa
  `iş × log n`, aşağı azalıyorsa tepe (`O(n)`), aşağı artıyorsa yapraklar.
- En büyük toplamlı alt dizi: sol, sağ, ortadan geçen; `O(n log n)`.
- Karatsuba: dört yerine üç çarpım; `n²` yerine `n^1,58`.
- En yakın nokta çifti: böl, `d`, yalnızca şeridi denetle; `O(n log n)`.
- Parçalar örtüşüyorsa dinamik programlama.
