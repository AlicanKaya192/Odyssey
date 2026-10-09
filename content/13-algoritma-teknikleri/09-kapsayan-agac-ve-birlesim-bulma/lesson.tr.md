# Kapsayan Ağaç ve Birleşim-Bulma

Altı şehri fiber kabloyla bağlayacaksın. Her şehir çiftinin kablo maliyeti
farklı ve her şehre bir yoldan ulaşmak yetiyor. En ucuz ağ hangisi? Bu
**en küçük kapsayan ağaç (minimum spanning tree, MST)** problemi: bütün
düğümleri bağlayan, döngüsü olmayan ve ağırlık toplamı en küçük kenar kümesi.

<figure class="fig">
<svg viewBox="0 0 530 250" width="530" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="69.1" y1="119.1" x2="169.2" y2="61.9"/>
<text class="dim" x="126.0" y="104.4" font-size="12" text-anchor="middle">4</text>
<line class="curve" x1="69.1" y1="140.9" x2="169.2" y2="198.1"/>
<text class="dim" x="114.0" y="184.4" font-size="12" text-anchor="middle">3</text>
<line class="curve" x1="190.0" y1="72.0" x2="190.0" y2="186.0"/>
<text class="dim" x="178.0" y="134.0" font-size="12" text-anchor="middle">2</text>
<line class="curve" x1="212.0" y1="50.0" x2="316.0" y2="50.0"/>
<text class="dim" x="265.0" y="66.0" font-size="12" text-anchor="middle">5</text>
<line class="line" x1="205.0" y1="194.0" x2="323.6" y2="67.5"/>
<text class="dim" x="273.8" y="142.2" font-size="12" text-anchor="middle">7</text>
<line class="line" x1="212.0" y1="210.0" x2="316.0" y2="210.0"/>
<text class="dim" x="265.0" y="226.0" font-size="12" text-anchor="middle">6</text>
<line class="curve" x1="340.0" y1="72.0" x2="340.0" y2="186.0"/>
<text class="dim" x="328.0" y="134.0" font-size="12" text-anchor="middle">1</text>
<line class="curve" x1="359.1" y1="60.9" x2="459.2" y2="118.1"/>
<text class="dim" x="404.0" y="104.4" font-size="12" text-anchor="middle">3</text>
<line class="line" x1="359.1" y1="199.1" x2="459.2" y2="141.9"/>
<text class="dim" x="416.0" y="184.4" font-size="12" text-anchor="middle">4</text>
<circle class="box" cx="50" cy="130" r="22"/>
<text class="ink" x="50" y="134.6" font-size="13" text-anchor="middle">A</text>
<circle class="box" cx="190" cy="50" r="22"/>
<text class="ink" x="190" y="54.5" font-size="13" text-anchor="middle">B</text>
<circle class="box" cx="190" cy="210" r="22"/>
<text class="ink" x="190" y="214.6" font-size="13" text-anchor="middle">C</text>
<circle class="box" cx="340" cy="50" r="22"/>
<text class="ink" x="340" y="54.5" font-size="13" text-anchor="middle">D</text>
<circle class="box" cx="340" cy="210" r="22"/>
<text class="ink" x="340" y="214.6" font-size="13" text-anchor="middle">E</text>
<circle class="box" cx="480" cy="130" r="22"/>
<text class="ink" x="480" y="134.6" font-size="13" text-anchor="middle">F</text>
</svg>
<figcaption>Altı şehir, dokuz olası kablo. Mor kenarlar en küçük kapsayan ağaç: beş kenar, toplam 14.</figcaption>
</figure>

`n` düğümlü bir kapsayan ağaçta her zaman `n − 1` kenar vardır: bir kenar
eksik olsa graf kopar, bir kenar fazla olsa döngü oluşur. Bu bölümdeki iki
yöntem (Kruskal ve Prim) de **açgözlü**: her adımda en ucuz uygun kenarı
alırlar ve ikisi de en iyi ağacı bulur.

## Birleşim-Bulma: kim hangi grupta?

Kruskal'ın sorduğu tek soru şu: "Bu kenarın iki ucu zaten bağlı mı?" Bağlıysa
kenar bir döngü kurar. Bunu her seferinde grafı gezerek sormak yavaş olur.
**Birleşim-bulma (union-find, disjoint set union, DSU)** yapısı iki işi çok
hızlı yapar:

- `find(x)`: `x`'in grubunun **temsilcisi** (kökü).
- `union(a, b)`: iki grubu birleştir; zaten aynı gruptaysa `False`.

Her öğe bir **ebeveyne** bakar; kök kendi ebeveynidir. Aynı köke çıkan öğeler
aynı gruptadır.

```python
class DSU:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # yolu kısalt
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                       # zaten aynı grupta
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                   # küçük grup büyüğün altına
        self.size[ra] += self.size[rb]
        return True


dsu = DSU("ABCDEF")
dsu.union("A", "B")
dsu.union("C", "D")
dsu.union("B", "D")
print(dsu.find("A") == dsu.find("C"), dsu.find("E") == dsu.find("F"))
print(dsu.union("A", "C"))
```

```text
True False
False
```

`A` ile `C` hiç doğrudan birleştirilmedi ama `B` ile `D` üzerinden aynı
gruptalar. Son satır `False`: o kenar bir döngü kurardı.

## İki küçük hile, büyük fark

Yapıyı hızlı yapan iki ayrıntı var:

- **Boya göre birleştirme (union by size):** küçük grubun kökü büyüğün altına
  gider; ağaç derinleşmez.
- **Yol kısaltma (path compression):** `find` yukarı çıkarken geçtiği
  öğeleri köke yaklaştırır; sonraki sorgular kısalır.

İkisi olmadan, öğeler sırayla birleşince ağaç uzun bir zincire döner. Aşağıdaki
kod `0`–`1`, `1`–`2`, ... diye birleştirip sonra her öğenin kökünü soruyor ve
`find`'ın kaç adım yukarı çıktığını sayıyor:

```python
def count_hops(n, smart):
    parent, size = list(range(n)), [1] * n
    hops = 0

    def find(x):
        nonlocal hops
        while parent[x] != x:
            if smart:
                parent[x] = parent[parent[x]]
            x = parent[x]
            hops += 1
        return x

    for i in range(n - 1):
        a, b = find(i), find(i + 1)
        if smart and size[a] > size[b]:
            a, b = b, a
        parent[a] = b                  # a'nın kökü b'nin altına
        size[b] += size[a]
    for i in range(n):
        find(i)
    return hops


for n in (1000, 5000):
    print(n, count_hops(n, False), count_hops(n, True))
```

```text
1000 499500 1996
5000 12497500 9996
```

Hilesiz sürümde adım sayısı `n²` gibi büyüyor (5 kat öğe, 25 kat adım);
hileli sürümde `n` gibi. İkisi birlikte kullanıldığında bir işlemin ortalama
maliyeti pratikte sabittir (kuramsal sınır `α(n)`, ters Ackermann fonksiyonu;
evrendeki atom sayısı kadar öğede bile 5'i geçmez).

## Kruskal: kenarları ucuzdan pahalıya

Kenarları ağırlığa göre sırala. Sırayla her kenara bak: iki ucu farklı
gruptaysa ağaca al ve grupları birleştir; aynı gruptaysa atla (döngü kurardı).

```python
edges = [(4, "A", "B"), (3, "A", "C"), (2, "B", "C"), (5, "B", "D"),
         (7, "C", "D"), (6, "C", "E"), (1, "D", "E"), (3, "D", "F"),
         (4, "E", "F")]                # (ağırlık, uç, uç)


def kruskal(nodes, edges):
    dsu = DSU(nodes)
    tree = []
    for w, a, b in sorted(edges):
        if dsu.union(a, b):            # farklı gruplar: döngü yok
            tree.append((a, b, w))
    return tree


tree = kruskal("ABCDEF", edges)
print(tree)
print("total", sum(w for _, _, w in tree), "of", sum(w for w, _, _ in edges))
```

```text
True False
False
[('D', 'E', 1), ('B', 'C', 2), ('A', 'C', 3), ('D', 'F', 3), ('B', 'D', 5)]
total 14 of 35
```

Dokuz kenarın toplamı 35, ağacınki 14. `A`–`B` (4) ve `E`–`F` (4) atlandı:
sıraları geldiğinde uçları zaten bağlıydı. Maliyet sıralamadan gelir:
`O(m log m)`.

## Prim: ağacı bir düğümden büyüt

Prim bir düğümden başlar ve her adımda **ağaçtan dışarı çıkan** en ucuz kenarı
ekler. En ucuz kenarı bulmak için heap: Dijkstra'ya çok benzer, ama heap'teki
sayı yolun toplamı değil yalnızca kenarın ağırlığıdır.

```python
import heapq


def prim(nodes, edges, start):
    adj = {n: [] for n in nodes}
    for w, a, b in edges:
        adj[a].append((w, b))
        adj[b].append((w, a))
    seen = {start}
    heap = [(w, start, b) for w, b in adj[start]]
    heapq.heapify(heap)
    tree = []
    while heap and len(seen) < len(adj):
        w, a, b = heapq.heappop(heap)
        if b in seen:
            continue                   # iki ucu da ağaçta: döngü kurardı
        seen.add(b)
        tree.append((a, b, w))
        for w2, c in adj[b]:
            if c not in seen:
                heapq.heappush(heap, (w2, b, c))
    return tree


tree = prim("ABCDEF", edges, "A")
print(tree)
print("total", sum(w for _, _, w in tree))
```

```text
True False
False
[('A', 'C', 3), ('C', 'B', 2), ('B', 'D', 5), ('D', 'E', 1), ('D', 'F', 3)]
total 14
```

Kenarlar farklı sırayla geldi ama ağaç ve toplam aynı: 14. Kruskal seyrek
graflarda ve kenar listesi elindeyken rahattır; Prim komşuluk listesiyle ve
yoğun graflarda iyi çalışır.

## Makine öğrenmesinde: tek bağlantılı kümeleme

Kruskal'ı **erken durdurursan** kümeleme yapmış olursun. Bütün nokta
çiftlerini uzaklığa göre sırala ve birleştir; grup sayısı `k`'ya inince dur.
Kalan gruplar **tek bağlantılı (single linkage) hiyerarşik kümelemenin**
sonucudur.

```python
import math
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score

points = [(1, 1), (2, 1), (1, 2), (2, 3), (8, 8), (9, 8), (8, 9),
          (9, 10), (1, 9), (2, 9), (2, 10)]


def single_link(points, k):
    n = len(points)
    pairs = sorted((math.dist(points[i], points[j]), i, j)
                   for i in range(n) for j in range(i + 1, n))
    dsu = DSU(range(n))
    groups = n
    for d, i, j in pairs:
        if groups == k:
            break
        if dsu.union(i, j):
            groups -= 1
    return [dsu.find(i) for i in range(n)]


labels = single_link(points, 3)
print(labels)
sk = AgglomerativeClustering(n_clusters=3, linkage="single").fit_predict(points)
print(adjusted_rand_score(labels, sk))
```

```text
True False
False
[0, 0, 0, 0, 4, 4, 4, 4, 8, 8, 8]
1.0
```

Grup numaraları farklı (bizimki temsilcinin sırası), ama
`adjusted_rand_score` 1.0: scikit-learn ile **aynı** gruplar. Tek bağlantı
uzun, ince kümeleri iyi bulur; aradaki tek bir köprü nokta ise iki kümeyi
birleştirebilir (zincirleme etkisi).

## Özet

- Kapsayan ağaç: bütün düğümler, `n − 1` kenar, döngü yok; MST en ucuzu.
- Birleşim-bulma: `find` ve `union`; boya göre birleştirme + yol kısaltma ile
  pratikte sabit süre.
- Kruskal: kenarları sırala, döngü kurmayanı al (`O(m log m)`).
- Prim: bir düğümden büyüt, heap ile en ucuz çıkan kenar.
- Kruskal'ı `k` grupta durdurmak = tek bağlantılı kümeleme.
