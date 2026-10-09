# Graf Gezinme

Ağaçlar bölümünde iki gezinme gördük: kuyrukla **genişlemesine (BFS)**,
yığınla ya da özyinelemeyle **derinlemesine (DFS)**. Graflarda ikisi de aynı
çalışır, tek bir farkla: grafta **döngü** olabilir. `ada → bora → cem →
ada` diye dönen bir yolda, nereye uğradığını tutmazsan sonsuza kadar dönersin.
Bu yüzden her graf gezinmesinin bir **ziyaret edilenler (visited)** kümesi
vardır.

<figure class="fig">
<svg viewBox="0 0 534 260" width="534" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="63.9" y1="38.2" x2="144.1" y2="32.0"/>
<line class="line" x1="53.8" y1="59.7" x2="95.1" y2="118.7"/>
<line class="line" x1="158.5" y1="51.1" x2="122.5" y2="117.2"/>
<line class="line" x1="185.0" y1="48.7" x2="233.8" y2="109.7"/>
<line class="line" x1="133.9" y1="138.3" x2="224.1" y2="131.9"/>
<line class="line" x1="272.6" y1="121.8" x2="335.6" y2="98.9"/>
<line class="line" x1="380.0" y1="103.3" x2="428.4" y2="135.6"/>
<line class="line" x1="403.3" y1="205.8" x2="474.8" y2="223.7"/>
<circle class="box" cx="40" cy="40" r="24"/>
<circle class="curve" cx="40" cy="40" r="24"/>
<text class="ink" x="40" y="44.2" font-size="12" text-anchor="middle">ada</text>
<circle class="box" cx="170" cy="30" r="24"/>
<text class="ink" x="170" y="34.2" font-size="12" text-anchor="middle">bora</text>
<circle class="box" cx="110" cy="140" r="24"/>
<text class="ink" x="110" y="144.2" font-size="12" text-anchor="middle">cem</text>
<circle class="box" cx="250" cy="130" r="24"/>
<text class="ink" x="250" y="134.2" font-size="12" text-anchor="middle">deniz</text>
<circle class="box" cx="360" cy="90" r="24"/>
<text class="ink" x="360" y="94.2" font-size="12" text-anchor="middle">ece</text>
<circle class="box" cx="450" cy="150" r="24"/>
<text class="ink" x="450" y="154.2" font-size="12" text-anchor="middle">fuat</text>
<circle class="box" cx="380" cy="200" r="24"/>
<text class="ink" x="380" y="204.2" font-size="12" text-anchor="middle">gul</text>
<circle class="box" cx="500" cy="230" r="24"/>
<text class="ink" x="500" y="234.2" font-size="12" text-anchor="middle">hakan</text>
</svg>
<figcaption>Bu bölümün grafı: iki kopuk parça. ada → bora → cem → ada bir döngü; gul ile hakan ayrı bir bileşen.</figcaption>
</figure>

```python
edges = [("ada", "bora"), ("ada", "cem"), ("bora", "cem"), ("bora", "deniz"),
         ("cem", "deniz"), ("deniz", "ece"), ("ece", "fuat"), ("gul", "hakan")]
graph = {}
for a, b in edges:
    graph.setdefault(a, set()).add(b)
    graph.setdefault(b, set()).add(a)
```

## BFS: en az adımlı yol

BFS başlangıçtan uzaklaşarak **kat kat** ilerler: önce bir adımda
ulaşılanlar, sonra iki adımda ulaşılanlar… Bu yüzden ağırlıksız bir grafta
bir düğüme **ilk ulaştığı yol, en az adımlı yoldur**.

```python
from collections import deque

def bfs_distances(graph, start):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in sorted(graph[node]):
            if neighbour not in distance:         # ilk ulaşma = en kısa
                distance[neighbour] = distance[node] + 1
                queue.append(neighbour)
    return distance

print(bfs_distances(graph, "ada"))
```

```text
{'ada': 0, 'bora': 1, 'cem': 1, 'deniz': 2, 'ece': 3, 'fuat': 4}
```

`distance` sözlüğü aynı zamanda ziyaret edilenler kümesi: bir düğüm sözlüğe
girdiyse bir daha kuyruğa girmez. Her düğüm ve her kenar bir kez işlenir:
`O(n + m)`.

## Yolu geri çıkarmak

Uzaklık yetmez, yolun kendisi gerekirse her düğüme **nereden geldiğini**
(ebeveynini) yaz; sonra hedeften geriye yürü.

```python
def shortest_path(graph, start, goal):
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            break
        for neighbour in sorted(graph[node]):
            if neighbour not in parent:
                parent[neighbour] = node
                queue.append(neighbour)
    if goal not in parent:
        return None                               # ulaşılamıyor
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]

print(shortest_path(graph, "ada", "fuat"))
print(shortest_path(graph, "ada", "gul"))
```

```text
['ada', 'bora', 'deniz', 'ece', 'fuat']
None
```

`gul` başka bir parçada: hiçbir yol yok.

## DFS: dibine kadar git

DFS bir yola girip gidebildiği kadar gider, sonra geri döner. Özyinelemeyle
kısa yazılır:

```python
def dfs(graph, node, visited, order):
    visited.add(node)
    order.append(node)
    for neighbour in sorted(graph[node]):
        if neighbour not in visited:
            dfs(graph, neighbour, visited, order)
    return order

print(dfs(graph, "ada", set(), []))
```

```text
['ada', 'bora', 'cem', 'deniz', 'ece', 'fuat']
```

Bu küçük grafta iki sıra aynı çıktı, ama yollar farklı: BFS `cem`'e
`ada`'dan doğrudan (1 adım) ulaştı, DFS ise önce `bora`'ya dalıp `cem`'e
oradan geldi (`ada → bora → cem`). İkisi de bütün ulaşılabilen
düğümleri `O(n + m)`'de gezer; fark sırada. **En az adım** gerekiyorsa BFS,
"bir yol var mı?", döngü bulma ve sıralama işleri için çoğu zaman DFS.

**Dikkat:** özyineli DFS uzun bir zincirde Python'un derinlik sınırına
takılır:

```text
recursive DFS on a chain of 5000 nodes: RecursionError
```

Büyük graflarda DFS de yığınla, özyinelemesiz yazılır (notta).

## Bağlı bileşenler

Graf birkaç kopuk parçadan oluşabilir. Her ziyaret edilmemiş düğümden yeni
bir gezinme başlatırsak her gezinme bir **bağlı bileşen (connected
component)** bulur:

```python
def components(graph):
    seen, groups = set(), []
    for start in sorted(graph):
        if start in seen:
            continue
        group, queue = [], deque([start])
        seen.add(start)
        while queue:
            node = queue.popleft()
            group.append(node)
            for neighbour in graph[node]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        groups.append(sorted(group))
    return groups

print(components(graph))
```

```text
[['ada', 'bora', 'cem', 'deniz', 'ece', 'fuat'], ['gul', 'hakan']]
```

Veri biliminde bağlı bileşenler sık iş görür: aynı müşteriye ait farklı
kayıtları birleştirmek (aynı e-posta ya da telefonu paylaşan kayıtlar bir
bileşen), sahtekârlık halkaları, sosyal ağdaki kopuk topluluklar.

## Izgarada en kısa yol

Bir labirent de graftır: her boş hücre bir düğüm, komşu hücreler kenar. BFS
çıkışa en az adımı bulur.

```python
def maze_steps(maze):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        r, c, steps = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return steps
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            inside = 0 <= nr < rows and 0 <= nc < cols
            if inside and maze[nr][nc] == "." and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc, steps + 1))
    return -1

maze = ["..#....",
        ".##.##.",
        "...#...",
        ".#...#.",
        "...#..."]
print(maze_steps(maze))
```

```text
10
```

## Özet

- Graf gezinmede ziyaret edilenler kümesi şart: döngüler sonsuz döngü yapar.
- BFS kuyrukla kat kat ilerler; ağırlıksız grafta en az adımlı yolu bulur.
- Yol için her düğümün ebeveynini tut, hedeften geriye yürü.
- DFS dibine kadar dalar; özyineli hâli derin graflarda sınıra takılır.
- Her gezinme bir bağlı bileşen bulur; kayıt birleştirme, topluluklar.
- Izgara ve labirentler de graftır. Hepsi `O(n + m)`.
