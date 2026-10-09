# En Kısa Yol

BFS kenar **sayısını** en aza indiriyordu. Gerçek hayatta kenarların
uzunluğu farklı: bir yol 2 km, öbürü 10 km. **Ağırlıklı** bir grafta en kısa
yol, toplam ağırlığı en küçük olan yoldur; harita uygulamaları, ağ
yönlendirme ve lojistik bunu çözer.

<figure class="fig">
<svg viewBox="0 0 480 250" width="480" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="57.6" y1="100.5" x2="150.6" y2="50.4"/>
<text class="dim" x="110.7" y="89.6" font-size="12" text-anchor="middle">4</text>
<line class="curve" x1="56.2" y1="121.8" x2="132.2" y2="177.1"/>
<text class="dim" x="87.9" y="163.7" font-size="12" text-anchor="middle">2</text>
<line class="curve" x1="167.4" y1="59.8" x2="152.9" y2="168.2"/>
<text class="dim" x="148.1" y="117.4" font-size="12" text-anchor="middle">1</text>
<line class="curve" x1="188.7" y1="47.2" x2="279.5" y2="82.1"/>
<text class="dim" x="230.7" y="80.2" font-size="12" text-anchor="middle">5</text>
<line class="line" x1="166.6" y1="178.9" x2="281.7" y2="102.2"/>
<text class="dim" x="231.7" y="154.0" font-size="12" text-anchor="middle">8</text>
<line class="line" x1="169.7" y1="193.3" x2="308.3" y2="216.4"/>
<text class="dim" x="238.0" y="220.8" font-size="12" text-anchor="middle">10</text>
<line class="curve" x1="304.5" y1="109.5" x2="325.1" y2="198.6"/>
<text class="dim" x="303.3" y="161.7" font-size="12" text-anchor="middle">2</text>
<line class="line" x1="319.0" y1="96.3" x2="429.1" y2="133.0"/>
<text class="dim" x="371.2" y="130.4" font-size="12" text-anchor="middle">6</text>
<line class="curve" x1="346.6" y1="208.9" x2="431.7" y2="152.2"/>
<text class="dim" x="396.7" y="194.0" font-size="12" text-anchor="middle">3</text>
<circle class="box" cx="40" cy="110" r="20"/>
<circle class="curve" cx="40" cy="110" r="20"/>
<text class="ink" x="40" y="114.5" font-size="13" text-anchor="middle">A</text>
<circle class="box" cx="170" cy="40" r="20"/>
<text class="ink" x="170" y="44.5" font-size="13" text-anchor="middle">B</text>
<circle class="box" cx="150" cy="190" r="20"/>
<text class="ink" x="150" y="194.6" font-size="13" text-anchor="middle">C</text>
<circle class="box" cx="300" cy="90" r="20"/>
<text class="ink" x="300" y="94.5" font-size="13" text-anchor="middle">D</text>
<circle class="box" cx="330" cy="220" r="20"/>
<text class="ink" x="330" y="224.6" font-size="13" text-anchor="middle">E</text>
<circle class="box" cx="450" cy="140" r="20"/>
<circle class="curve4" cx="450" cy="140" r="20"/>
<text class="ink" x="450" y="144.6" font-size="13" text-anchor="middle">F</text>
</svg>
<figcaption>Bu bölümün ağırlıklı grafı. Mor kenarlar A'dan F'ye en kısa yol: 2 + 1 + 5 + 2 + 3 = 13.</figcaption>
</figure>

## Dijkstra

1959'dan beri kullanılan açgözlü bir algoritma: **henüz kesinleşmemiş en yakın
düğümü** al, onu kesinleştir, komşularının uzaklığını güncelle. "En yakın"ı
hızlı bulmak için heap.

```python
import heapq
import math

roads = {"A": {"B": 4, "C": 2},
         "B": {"A": 4, "C": 1, "D": 5},
         "C": {"A": 2, "B": 1, "D": 8, "E": 10},
         "D": {"B": 5, "C": 8, "E": 2, "F": 6},
         "E": {"C": 10, "D": 2, "F": 3},
         "F": {"D": 6, "E": 3}}

def dijkstra(graph, start):
    dist, parent = {start: 0}, {start: None}
    heap, done = [(0, start)], set()
    while heap:
        d, node = heapq.heappop(heap)
        if node in done:                       # eski, daha uzun bir kayıt
            continue
        done.add(node)                         # artık kesin
        for nxt, w in graph[node].items():
            if d + w < dist.get(nxt, math.inf):
                dist[nxt] = d + w
                parent[nxt] = node
                heapq.heappush(heap, (d + w, nxt))
    return dist, parent

dist, parent = dijkstra(roads, "A")
print(dict(sorted(dist.items())))
path = ["F"]
while parent[path[-1]] is not None:
    path.append(parent[path[-1]])
print(path[::-1])
```

```text
{'A': 0, 'B': 3, 'C': 2, 'D': 8, 'E': 10, 'F': 13}
['A', 'C', 'B', 'D', 'E', 'F']
```

`A`'dan `B`'ye doğrudan kenar 4, ama `A → C → B` 3: Dijkstra kısa yolu buldu.
Heap'ten çıkan ilk kayıt en kısasıdır, çünkü bütün kenarlar **negatif
değil**: daha sonra bulunacak bir yol ancak daha uzun olabilir. Bir düğüm heap'e
birkaç kez girebilir; `done` kümesi eskileri atlar. Maliyet
`O((n + m) log n)`.

## Negatif kenar: Dijkstra yanılır

Kenarlardan biri negatifse (bir indirim, bir enerji kazancı) Dijkstra'nın
"kesinleşti" varsayımı bozulur:

```python
negative = {"S": {"A": 1, "B": 4}, "A": {"C": 3}, "B": {"A": -4}, "C": {}}
print(dict(sorted(dijkstra(negative, "S")[0].items())))

def bellman_ford(graph, start):
    dist = {node: math.inf for node in graph}
    dist[start] = 0
    for _ in range(len(graph) - 1):            # n − 1 tur
        for a in graph:
            for b, w in graph[a].items():
                if dist[a] + w < dist[b]:
                    dist[b] = dist[a] + w
    return dist

print(dict(sorted(bellman_ford(negative, "S").items())))
```

```text
{'A': 0, 'B': 4, 'C': 4, 'S': 0}
{'A': 0, 'B': 4, 'C': 3, 'S': 0}
```

Doğru cevapta `C` 3 (`S → B → A → C = 4 − 4 + 3`). Dijkstra `A`'yı 1 ile
kesinleştirip `C`'yi 4 bıraktı; `B` üzerinden gelen daha kısa yol `A`'yı
güncellese de `C`'ye yayılmadı. **Bellman–Ford** her kenarı `n − 1` tur
gevşetir; negatif kenarda doğru çalışır ama `O(n · m)`. (Toplamı negatif bir
döngü varsa "en kısa yol" tanımsızdır; Bellman–Ford fazladan bir turla bunu
da yakalar.)

## Bütün çiftler: Floyd–Warshall

Her düğümden her düğüme uzaklık gerekiyorsa (bir uzaklık tablosu, kümeleme
için uzaklık matrisi) **Floyd–Warshall** üç iç içe döngüyle hepsini bulur:
"`k` üzerinden geçmek daha kısa mı?"

```python
def floyd_warshall(graph):
    nodes = sorted(graph)
    d = {a: {b: graph[a].get(b, math.inf) for b in nodes} for a in nodes}
    for a in nodes:
        d[a][a] = 0
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d

table = floyd_warshall(roads)
print(table["A"]["F"], table["B"]["E"])
```

```text
13 7
```

`O(n³)`: birkaç yüz düğüme kadar rahat, çok büyük graflarda her düğümden
Dijkstra daha iyi.

## A*: hedefi bilerek aramak

Dijkstra hedefin nerede olduğunu bilmez; her yöne eşit yayılır. **A***
her düğüme bir **tahmin** ekler: "buradan hedefe en az bu kadar var". Izgarada
Manhattan uzaklığı (`|Δsatır| + |Δsütun|`) böyle bir tahmin. Heap'te sıra
`gelinen yol + tahmin`'e göre olunca arama hedefe doğru akar.

```text
open 60x60 grid  : path 118 | Dijkstra 3444 nodes | A* 200 nodes
60x60 maze       : path 502 | Dijkstra 2682 nodes | A* 2503 nodes
```

Tahmin gerçek uzaklığı **hiç aşmadığı** sürece A* yine en kısa yolu bulur.
Açık bir ızgarada açılan düğüm sayısı on yedi kat azaldı; duvarlarla dolu,
yolun hedeften uzaklaşıp döndüğü bir labirentte tahmin az işe yaradı.
Oyunlardaki yol bulma ve harita uygulamaları A*'ın çeşitlerini kullanır.

## Özet

- Ağırlıklı en kısa yol: Dijkstra, heap ile `O((n + m) log n)`; kenarlar
  negatif olmamalı.
- Yol için ebeveynleri tut, hedeften geriye yürü.
- Negatif kenar: Bellman–Ford, `O(n · m)`; negatif döngüyü de yakalar.
- Bütün çiftler: Floyd–Warshall, `O(n³)`.
- A*: Dijkstra + hedefe tahmin; tahmin abartmazsa yine en kısa.
