# Açgözlü Algoritmalar

**Açgözlü (greedy)** bir algoritma her adımda **o an en iyi görüneni** seçer
ve bir daha geri dönmez. Geri izleme bütün yolları deniyordu; açgözlü yöntem
tek bir yol yürür. Bu yüzden çok hızlı ve yazması kolay. Ama bedeli büyük:
her problemde doğru sonucu vermez. Bu bölümün iki sorusu var:

1. Açgözlü seçim bu problemde **gerçekten** en iyiyi veriyor mu?
2. Vermiyorsa, ne kadar kötü?

## Para üstü

Kasada 87 sent para üstü vereceksin; elindeki madeni paralar 1, 5, 10, 25 ve
50 sent. En az sayıda para için akla gelen ilk yol: her seferinde sığan **en
büyük** parayı ver.

```python
def greedy_change(amount, coins):
    used = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            used.append(coin)
    return used

print(greedy_change(87, [1, 5, 10, 25, 50]))
print(greedy_change(6, [1, 3, 4]))
```

```text
[50, 25, 10, 1, 1]
[4, 1, 1]
```

İlk sistemde beş para, ve bu gerçekten en azı. İkinci sistemde açgözlü yol
`4 + 1 + 1` diye **üç** para verdi; oysa `3 + 3` **iki** para. İlk adımda en
büyüğü (4) almak, sonraki adımları kötü bir duruma soktu. Para sistemleri
çoğunlukla açgözlünün doğru çalışacağı şekilde tasarlanır; rastgele bir
sistemde en azını bulmak için bir sonraki bölümün **dinamik programlaması**
gerekir.

## Toplantı seçimi

Tek bir toplantı odası var ve gün içinde birçok toplantı isteği geldi. Çakışan
iki toplantı aynı anda yapılamaz. **En çok sayıda** toplantıyı sığdırmak
istiyoruz. Üç açgözlü kural akla geliyor:

- **Erken başlayan önce:** sabah ilk başlayan toplantıyı al.
- **Kısa olan önce:** odayı en az meşgul edeni al.
- **Erken biten önce:** odayı en erken boşaltanı al.

Her kural aynı şekilde çalışır: toplantıları o kurala göre sırala, sırayla
bak, seçilenlerle çakışmıyorsa al.

Hangisi doğru? İki küçük karşı örnek ve 200 rastgele günün ortalaması:

```python
def pick(meetings, key):
    chosen = []
    for start, end in sorted(meetings, key=key):
        if all(end <= s or start >= e for s, e in chosen):   # çakışmıyor
            chosen.append((start, end))
    return len(chosen)

by_end = lambda m: m[1]
by_start = lambda m: m[0]
by_length = lambda m: m[1] - m[0]

for day in ([(9, 17), (10, 11), (11, 12), (12, 13)], [(1, 5), (4, 7), (6, 10)]):
    print(pick(day, by_end), pick(day, by_start), pick(day, by_length))
```

```text
3 1 3
2 2 1
```

```text
average over 200 days, 40 requests each
earliest end first  : 9.665
earliest start first: 6.285
shortest first      : 9.515
days another rule beat earliest end: 0
```

**Erken başlayan önce** sabah 9'dan akşam 5'e süren tek toplantıya takıldı.
**Kısa olan önce** ikinci günde ortadaki kısa toplantıyı seçip iki uzunu
kaçırdı. **Erken biten önce** her iki günde de en iyisini buldu ve 200
rastgele günün hiçbirinde öbür iki kural onu geçemedi.

Neden doğru? Herhangi bir en iyi çözümün ilk toplantısını, en erken biten
toplantıyla değiştir: o daha erken bittiği için geri kalanların hiçbiriyle
çakışmaz ve sayı azalmaz. Bu **değiştirme (exchange) argümanı**, açgözlü
seçimlerin doğruluğunu göstermenin klasik yolu. Erken biten önce seçildiği
için toplam iş sıralama kadar: `O(n log n)`.

## Sırt çantası: kesirli ve bütün

Çantan 50 kilo taşıyor. Üç eşya var (değer, ağırlık): `(60, 10)`,
`(100, 20)`, `(120, 30)`. Açgözlü kural: **kilo başına değeri** en yüksek
olandan başla.

- **Kesirli** sırt çantasında eşyayı bölebilirsin (un, altın tozu). Açgözlü
  kural kesin en iyiyi verir.
- **Bütün (0/1)** sırt çantasında eşya ya tamamen girer ya hiç. Aynı kural
  yanılabilir.

```python
items = [(60, 10), (100, 20), (120, 30)]       # (değer, ağırlık)

def fractional(items, capacity):
    total = 0
    for value, weight in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        take = min(weight, capacity)
        total += value * take / weight
        capacity -= take
    return total

def greedy_whole(items, capacity):
    total = 0
    for value, weight in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        if weight <= capacity:
            total += value
            capacity -= weight
    return total

print(fractional(items, 50), greedy_whole(items, 50))
```

```text
240.0 160
```

Bütün eşyalarda açgözlü yol 160 buldu (ilk iki eşya), oysa ikinci ve
üçüncü eşya birlikte 220 değer ediyor. Bütün sırt çantasının doğru çözümü de
dinamik programlamada.

## Huffman kodlaması

Bir metni bitlerle saklarken her harfe 8 bit vermek yerine **sık geçen harfe
kısa, seyrek geçene uzun** kod verirsek metin küçülür. Huffman'ın 1952'deki
açgözlü algoritması bunun en iyisini bulur: her adımda **en seyrek iki
grubu** birleştir.

```python
import heapq
from collections import Counter

def huffman(text):
    counts = sorted(Counter(text).items())
    heap = [(n, i, {ch: ""}) for i, (ch, n) in enumerate(counts)]
    heapq.heapify(heap)
    order = len(heap)
    while len(heap) > 1:
        n1, _, left = heapq.heappop(heap)       # en seyrek iki grup
        n2, _, right = heapq.heappop(heap)
        merged = {ch: "0" + code for ch, code in left.items()}
        merged.update({ch: "1" + code for ch, code in right.items()})
        heapq.heappush(heap, (n1 + n2, order, merged))
        order += 1
    return heap[0][2]

text = "abracadabra"
codes = huffman(text)
print(sorted(codes.items()))
print(sum(len(codes[ch]) for ch in text), "bits instead of", 8 * len(text))
```

```text
[('a', '0'), ('b', '110'), ('c', '100'), ('d', '101'), ('r', '111')]
23 bits instead of 88
```

<figure class="fig">
<svg viewBox="0 0 549 244" width="549" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="204.7" y1="153.0" x2="146.7" y2="217.0"/>
<text class="dim" x="165.7" y="185.0" font-size="12" text-anchor="end">0</text>
<line class="line" x1="204.7" y1="153.0" x2="262.7" y2="217.0"/>
<text class="dim" x="243.7" y="185.0" font-size="12" text-anchor="start">1</text>
<line class="line" x1="436.7" y1="153.0" x2="378.7" y2="217.0"/>
<text class="dim" x="397.7" y="185.0" font-size="12" text-anchor="end">0</text>
<line class="line" x1="436.7" y1="153.0" x2="494.7" y2="217.0"/>
<text class="dim" x="475.7" y="185.0" font-size="12" text-anchor="start">1</text>
<line class="line" x1="320.7" y1="89.0" x2="204.7" y2="153.0"/>
<text class="dim" x="252.7" y="121.0" font-size="12" text-anchor="end">0</text>
<line class="line" x1="320.7" y1="89.0" x2="436.7" y2="153.0"/>
<text class="dim" x="388.7" y="121.0" font-size="12" text-anchor="start">1</text>
<line class="line" x1="88.7" y1="25.0" x2="30.7" y2="89.0"/>
<text class="dim" x="49.7" y="57.0" font-size="12" text-anchor="end">0</text>
<line class="line" x1="88.7" y1="25.0" x2="320.7" y2="89.0"/>
<text class="dim" x="214.7" y="57.0" font-size="12" text-anchor="start">1</text>
<rect class="box" x="6.0" y="72.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="6.0" y="72.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="30.7" y="93.9" font-size="14" text-anchor="middle">a: 5</text>
<circle class="box" cx="88.7" cy="25.0" r="17"/>
<text class="ink" x="88.7" y="29.9" font-size="14" text-anchor="middle">11</text>
<rect class="box" x="122.0" y="200.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="122.0" y="200.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="146.7" y="221.9" font-size="14" text-anchor="middle">c: 1</text>
<circle class="box" cx="204.7" cy="153.0" r="17"/>
<text class="ink" x="204.7" y="157.9" font-size="14" text-anchor="middle">2</text>
<rect class="box" x="238.0" y="200.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="238.0" y="200.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="262.7" y="221.9" font-size="14" text-anchor="middle">d: 1</text>
<circle class="box" cx="320.7" cy="89.0" r="17"/>
<text class="ink" x="320.7" y="93.9" font-size="14" text-anchor="middle">6</text>
<rect class="box" x="354.0" y="200.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="354.0" y="200.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="378.7" y="221.9" font-size="14" text-anchor="middle">b: 2</text>
<circle class="box" cx="436.7" cy="153.0" r="17"/>
<text class="ink" x="436.7" y="157.9" font-size="14" text-anchor="middle">4</text>
<rect class="box" x="470.0" y="200.0" width="49.4" height="34" rx="8"/>
<rect class="curve4" x="470.0" y="200.0" width="49.4" height="34" rx="8"/>
<text class="ink" x="494.7" y="221.9" font-size="14" text-anchor="middle">r: 2</text>
</svg>
<figcaption>abracadabra'nın Huffman ağacı. Yapraklarda harf ve sayısı; kökten yaprağa yoldaki 0 ve 1'ler o harfin kodu (b = 110).</figcaption>
</figure>

Beş kez geçen `a` tek bitlik `0`, birer kez geçen `c` ve `d` üç bitlik.
Hiçbir kod başka bir kodun başlangıcı değil (**önek koşulu**), bu yüzden
bitler ayraçsız yan yana yazılıp tek anlamla okunabiliyor. ZIP, PNG ve MP3
dosyalarının içinde bu fikir çalışır. Heap kullanıldığı için `k` farklı
harfte `O(k log k)`.

## Veri biliminde açgözlü seçimler

**İleri özellik seçimi (forward selection):** 30 özelliğin bütün alt
kümelerini denemek bir milyardan fazla model demekti (Geri İzleme bölümü).
Açgözlü yol: her adımda **modele en çok katkı yapan** özelliği ekle. Altı
özellikli yapay bir veride (gerçek ilişki 0, 2 ve 4. özelliklerde):

```python
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(300, 6))
y = 3 * X[:, 0] - 2 * X[:, 2] + 0.5 * X[:, 4] + rng.normal(scale=0.5, size=300)

def r2(cols):                                    # doğrusal regresyonun R²'si
    A = np.column_stack([X[:, cols], np.ones(len(y))])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    residual = y - A @ coef
    return 1 - (residual ** 2).sum() / ((y - y.mean()) ** 2).sum()

chosen = []
for step in range(3):
    best = max((c for c in range(6) if c not in chosen), key=lambda c: r2(chosen + [c]))
    chosen.append(best)
    print(step + 1, chosen, round(r2(chosen), 3))
```

```text
1 [0] 0.642
2 [0, 2] 0.965
3 [0, 2, 4] 0.981
```

Üç adımda doğru üç özellik, `2⁶ = 64` yerine `6 + 5 + 4 = 15` model. Ama
garanti yok: tek başına zayıf görünüp başkasıyla birlikte güçlü olan
özellikleri açgözlü seçim kaçırabilir.

**Karar ağaçları** da açgözlüdür: her düğümde **o an** en iyi bölmeyi seçer,
sonraki bölmeleri düşünmez. En iyi ağacı bulmak çok zor bir problem; açgözlü
bölme bu yüzden kullanılır ve çoğu zaman yeterince iyidir.

## Özet

- Açgözlü: her adımda o an en iyi görüneni seç, geri dönme; hızlı ve basit.
- Doğruluğu ispat ister (değiştirme argümanı); karşı örnek bulmak çoğu zaman
  kolay.
- Çalıştığı yerler: toplantı seçimi (erken biten önce), kesirli sırt
  çantası, Huffman, kanonik para sistemleri.
- Yanıldığı yerler: rastgele para sistemi, bütün (0/1) sırt çantası; doğrusu
  dinamik programlamada.
- Veri biliminde: ileri özellik seçimi ve karar ağacı bölmeleri açgözlü.
