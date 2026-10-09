# Problem Çözme Kalıpları

Yeni bir problemle karşılaşınca çoğu zaman sıfırdan bir algoritma icat
etmezsin; problemin hangi **kalıba** benzediğini tanırsın. Bu bölüm iki şey
yapıyor: önce girdinin boyutundan hangi karmaşıklığın yeteceğini kestirmeyi,
sonra şimdiye kadar görmediğimiz dört kalıbı ölçerek gösteriyor.

## Önce bütçe: girdinin boyu ne söylüyor?

Python bir döngüde saniyede kabaca on milyon civarında basit adım atar
(makineye göre birkaç kat değişir). Girdinin boyu, hangi
karmaşıklığın sığacağını büyük ölçüde belirler:

| `n` en fazla | Sığan karmaşıklık | Akla gelen kalıp |
|---|---|---|
| ~20 | `O(2ⁿ)` | bütün alt kümeler, geri izleme |
| ~40 | `O(2^(n/2))` | ortada buluşma |
| ~1 000 | `O(n²)` | iç içe döngü, DP tablosu |
| ~1 000 000 | `O(n log n)`, `O(n)` | sıralama, iki işaretçi, hash, yığın |
| çok büyük | `O(log n)`, `O(1)` | ikili arama, formül |

Bu tablo kesin bir kural değil, bir başlangıç noktası: `n = 100 000` görürsen
iç içe döngüyü baştan elersin.

## Cevap üzerinde ikili arama

"En az kaç?" ya da "en çok kaç?" diye soran bazı problemlerde cevabı doğrudan
bulmak zordur, ama bir aday cevabın **yetip yetmediğini** denetlemek kolaydır.
Denetim **tek yönlü** ise (yeten bir değerden büyükleri de yeter), cevap
üzerinde ikili arama yapılır.

Örnek: kutular sırayla gemiye yükleniyor, her gün en fazla `capacity` kadar.
`days` günde bitmesi için en küçük kapasite ne?

```python
def days_needed(weights, capacity):
    days, load = 1, 0
    for w in weights:
        if load + w > capacity:            # sığmıyor: yeni gün
            days, load = days + 1, 0
        load += w
    return days


def min_capacity(weights, days):
    lo, hi = max(weights), sum(weights)    # cevap bu aralıkta
    checks = 0
    while lo < hi:
        mid = (lo + hi) // 2
        checks += 1
        if days_needed(weights, mid) <= days:
            hi = mid                       # yetiyor: daha küçüğü dene
        else:
            lo = mid + 1                   # yetmiyor: daha büyük gerek
    return lo, checks


boxes = [3, 2, 2, 4, 1, 4, 5, 3, 7, 6]
print(min_capacity(boxes, 3))
import random
random.seed(2)
big = [random.randint(1, 1000) for _ in range(100_000)]
cap, checks = min_capacity(big, 50)
print(cap, checks, sum(big) - max(big))
```

```text
(13, 5)
1000274 25 49994662
```

Yüz bin kutuda aday aralık yaklaşık 50 milyon değer; her adayı sırayla denemek
50 milyon kez yüz bin kutuyu gezmek demek. İkili arama 25 denetimde buldu:
`O(n log S)`, `S` aralığın genişliği.

## Monoton yığın

"Her gün için, daha sıcak bir güne kaç gün var?" Saf yol her günden ileriye
bakar: `O(n²)`. **Monoton yığın** cevabı henüz bulunmamış günleri, sıcaklıkları
azalan sırada bir yığında tutar. Yeni gün yığının tepesindekinden sıcaksa, o
günün cevabı bulunmuştur: çıkar.

```python
def next_warmer_slow(temps):
    result, comps = [0] * len(temps), 0
    for i in range(len(temps)):
        for j in range(i + 1, len(temps)):
            comps += 1
            if temps[j] > temps[i]:
                result[i] = j - i
                break
    return result, comps


def next_warmer(temps):
    result, stack, comps = [0] * len(temps), [], 0
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            comps += 1
            j = stack.pop()                # j'nin cevabı bulundu
            result[j] = i - j
        stack.append(i)
    return result, comps


temps = [22, 21, 23, 20, 19, 24, 25, 18]
print(next_warmer(temps)[0])
falling = list(range(5000, 0, -1)) + [9999]
print(next_warmer_slow(falling)[1], next_warmer(falling)[1])
```

```text
[2, 1, 3, 2, 1, 1, 0, 0]
12502500 5000
```

Sürekli soğuyan beş bin gün ve sonunda sıcak bir gün: saf yol 12,5 milyon,
yığın 5000 karşılaştırma. Her gün yığına bir kez girip bir kez çıktığı için
`O(n)`. Aynı kalıp "bir sonraki büyük eleman", histogramdaki en büyük
dikdörtgen ve hisse fiyatı aralığı sorularında çıkar.

## Durum uzayında BFS

Bazı bulmacalarda graf açıkça verilmez: **durumlar** düğüm, **hamleler**
kenardır. En az hamle sorusu ağırlıksız grafta en kısa yol olduğu için BFS
kullanılır.

Örnek: 3 ve 5 litrelik iki kova ile tam 4 litre ölç. Hamleler: bir kovayı
doldur, boşalt, birinden ötekine dök.

<figure class="fig">
<svg viewBox="0 0 540 80" width="540" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="dim" d="M0 0L10 5L0 10z"/></marker></defs>
<line class="line" x1="62.0" y1="40.0" x2="86.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="140.0" y1="40.0" x2="164.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="218.0" y1="40.0" x2="242.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="296.0" y1="40.0" x2="320.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="374.0" y1="40.0" x2="398.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="452.0" y1="40.0" x2="476.0" y2="40.0" marker-end="url(#arr)"/>
<circle class="box" cx="36" cy="40" r="26"/>
<text class="ink" x="36" y="44.2" font-size="12" text-anchor="middle">0,0</text>
<circle class="box" cx="114" cy="40" r="26"/>
<text class="ink" x="114" y="44.2" font-size="12" text-anchor="middle">0,5</text>
<circle class="box" cx="192" cy="40" r="26"/>
<text class="ink" x="192" y="44.2" font-size="12" text-anchor="middle">3,2</text>
<circle class="box" cx="270" cy="40" r="26"/>
<text class="ink" x="270" y="44.2" font-size="12" text-anchor="middle">0,2</text>
<circle class="box" cx="348" cy="40" r="26"/>
<text class="ink" x="348" y="44.2" font-size="12" text-anchor="middle">2,0</text>
<circle class="box" cx="426" cy="40" r="26"/>
<text class="ink" x="426" y="44.2" font-size="12" text-anchor="middle">2,5</text>
<circle class="box" cx="504" cy="40" r="26"/>
<circle class="curve4" cx="504" cy="40" r="26"/>
<text class="ink" x="504" y="44.2" font-size="12" text-anchor="middle">3,4</text>
</svg>
<figcaption>Durum = (3 litrelikte, 5 litrelikte). 5'i doldur, 3'e dök, 3'ü boşalt, kalan 2'yi 3'e aktar, 5'i doldur, 3'ü tamamla: 5 litrelikte 4 litre kalır.</figcaption>
</figure>

```python
from collections import deque


def jug_steps(a, b, goal):
    start = (0, 0)
    prev = {start: None}                   # hem görüldü hem geri iz
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if goal in (x, y):
            path, state = [], (x, y)
            while state:
                path.append(state)
                state = prev[state]
            return path[::-1]
        pour_xy = min(x, b - y)
        pour_yx = min(y, a - x)
        for nxt in [(a, y), (x, b), (0, y), (x, 0),
                    (x - pour_xy, y + pour_xy), (x + pour_yx, y - pour_yx)]:
            if nxt not in prev:
                prev[nxt] = (x, y)
                queue.append(nxt)
    return None


print(jug_steps(3, 5, 4))
print(jug_steps(2, 4, 3))
```

```text
[(0, 0), (0, 5), (3, 2), (0, 2), (2, 0), (2, 5), (3, 4)]
None
```

Altı hamle; BFS bundan kısa yol olmadığını garanti eder. 2 ve 4 litrelik
kovalarla 3 litre ise imkânsız: bütün durumlar gezilip bitti. (Kovalarla
yalnızca hacimlerin EBOB'unun katları ölçülebilir; `gcd(2, 4) = 2`.)

## Ortada buluşma

36 eşyanın bütün alt kümelerini denemek `2³⁶` ≈ 69 milyar alt küme demek.
**Ortada buluşma (meet in the middle)** eşyaları ikiye böler: her yarının
`2¹⁸` alt küme toplamı ayrı ayrı hesaplanır, biri sıralanır ve öteki
yarıdaki her toplam için ikili aramayla eş aranır.

```python
from bisect import bisect_right


def subset_sums(items):
    sums = [0]
    for x in items:
        sums += [s + x for s in sums]      # her eşya: al ya da alma
    return sums


def count_at_most(items, limit):
    half = len(items) // 2
    left = subset_sums(items[:half])
    right = sorted(subset_sums(items[half:]))
    count = sum(bisect_right(right, limit - s) for s in left)
    return count, len(left) + len(right)


random.seed(5)
items = [random.randint(1, 1000) for _ in range(36)]
count, work = count_at_most(items, 9000)
print(count, work, 2 ** 36)
small = items[:16]
brute = sum(1 for mask in range(2 ** 16)
            if sum(small[i] for i in range(16) if mask >> i & 1) <= 4000)
print(brute, count_at_most(small, 4000)[0])
```

```text
27684403632 524288 68719476736
12718 12718
```

Toplamı 9000'i geçmeyen 27,7 milyar alt küme, yalnızca yaklaşık yarım milyon
toplam hesaplanarak sayıldı. Son satır, kaba kuvvetin yetişebildiği 16 eşyada
iki yolun aynı cevabı verdiğini doğruluyor.

## Kalıbı tanımak

| Problemde şu varsa | Dene |
|---|---|
| "en az / en çok" + adayı denetlemek kolay | cevap üzerinde ikili arama |
| "bir sonraki büyük / küçük" | monoton yığın |
| "en az hamle", durumlar ve hamleler | durum uzayında BFS |
| `n` ~40, alt kümeler | ortada buluşma |
| alt dizi toplamı, aralık sorgusu | önek toplamı (Temel Algoritmalar) |
| sıralı dizide çift, pencere | iki işaretçi, kayan pencere (Temel Algoritmalar) |
| "kaç yol / en iyi" + örtüşen alt problemler | dinamik programlama |
| her adımda yerel en iyi seçim güvenli | açgözlü |

## Makine öğrenmesinde

- Cevap üzerinde ikili arama: bir modelin istenen kesinliği tutturduğu **en
  küçük eşik** ya da bellek sınırına sığan en büyük grup boyu böyle bulunur.
- Monoton yığın: zaman serilerinde "bir sonraki tepe" ve geri çekilme
  (drawdown) hesapları.
- Durum uzayında arama: oyun oynayan ve planlama yapan ajanlar (pekiştirmeli
  öğrenmenin klasik arka planı).

## Özet

- Önce girdinin boyuyla karmaşıklık bütçesini kestir.
- Tek yönlü bir denetim varsa cevap üzerinde ikili arama.
- "Bir sonraki büyük" sorularında monoton yığın, `O(n)`.
- En az hamle sorularında durumları düğüm sayıp BFS.
- `n` ~40'ta alt kümeleri ikiye bölüp ortada buluş.
