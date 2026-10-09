# Graflar

Ağaçta her düğümün tek bir ebeveyni vardı. Gerçek dünyadaki ilişkilerin
çoğu böyle değil: bir sosyal ağda herkes birçok kişiyle arkadaş, bir yol
haritasında her kavşak birçok kavşağa bağlı, web sayfaları birbirine
bağlantı veriyor. Bu yapının adı **graf (graph)**: **düğümler (node,
vertex)** ve onları bağlayan **kenarlar (edge)**.

<figure class="fig">
<svg viewBox="0 0 484 184" width="484" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="63.9" y1="38.2" x2="144.1" y2="32.0"/>
<line class="line" x1="53.8" y1="59.7" x2="95.1" y2="118.7"/>
<line class="line" x1="158.5" y1="51.1" x2="122.5" y2="117.2"/>
<line class="line" x1="185.0" y1="48.7" x2="233.8" y2="109.7"/>
<line class="line" x1="133.9" y1="138.3" x2="224.1" y2="131.9"/>
<line class="line" x1="272.6" y1="121.8" x2="335.6" y2="98.9"/>
<line class="line" x1="380.0" y1="103.3" x2="428.4" y2="135.6"/>
<circle class="box" cx="40" cy="40" r="24"/>
<text class="ink" x="40" y="44.2" font-size="12" text-anchor="middle">ada</text>
<circle class="box" cx="170" cy="30" r="24"/>
<text class="ink" x="170" y="34.2" font-size="12" text-anchor="middle">bora</text>
<circle class="box" cx="110" cy="140" r="24"/>
<text class="ink" x="110" y="144.2" font-size="12" text-anchor="middle">cem</text>
<circle class="box" cx="250" cy="130" r="24"/>
<circle class="curve4" cx="250" cy="130" r="24"/>
<text class="ink" x="250" y="134.2" font-size="12" text-anchor="middle">deniz</text>
<circle class="box" cx="360" cy="90" r="24"/>
<text class="ink" x="360" y="94.2" font-size="12" text-anchor="middle">ece</text>
<circle class="box" cx="450" cy="150" r="24"/>
<text class="ink" x="450" y="154.2" font-size="12" text-anchor="middle">fuat</text>
</svg>
<figcaption>Altı kişilik bir arkadaşlık ağı. Yeşil halkalı deniz, ada'nın arkadaşı değil ama ikisinin iki ortak arkadaşı var.</figcaption>
</figure>

## Terimler

- **Komşu:** bir kenarla doğrudan bağlı düğüm. `cem`'in komşuları `ada`,
  `bora`, `deniz`.
- **Derece (degree):** bir düğümün kenar sayısı. Sosyal ağda arkadaş sayısı.
- **Yönsüz / yönlü:** arkadaşlık iki yönlüdür (yönsüz); bir hesabı **takip
  etmek** ya da bir sayfaya **bağlantı vermek** tek yönlüdür (yönlü). Yönlü
  grafta **giren** ve **çıkan** derece ayrıdır.
- **Ağırlıklı:** kenarın bir değeri var (yol uzunluğu, süre, ücret).
- **Yol:** kenarlarla birbirine bağlanan düğüm dizisi. `ada → cem → deniz`.
- **Bağlı:** her düğümden her düğüme bir yol varsa graf bağlıdır.

Ağaç, aslında döngüsü olmayan bağlı bir graf.

## Grafı koda dökmek

Üç yol var:

- **Kenar listesi:** `[("ada", "bora"), ...]`. Dosyada saklamak ve bir yerden
  okumak için doğal.
- **Komşuluk listesi (adjacency list):** her düğüm için komşularının listesi
  ya da kümesi. Python'da sözlük. En çok kullanılan.
- **Komşuluk matrisi (adjacency matrix):** `n × n` tablo; `A[i][j] = 1` ise
  `i` ile `j` arasında kenar var.

```python
edges = [("ada", "bora"), ("ada", "cem"), ("bora", "cem"), ("bora", "deniz"),
         ("cem", "deniz"), ("deniz", "ece"), ("ece", "fuat")]

graph = {}
for a, b in edges:                       # yönsüz: iki yöne de ekle
    graph.setdefault(a, set()).add(b)
    graph.setdefault(b, set()).add(a)

for node in sorted(graph):
    print(node, sorted(graph[node]))
```

```text
ada ['bora', 'cem']
bora ['ada', 'cem', 'deniz']
cem ['ada', 'bora', 'deniz']
deniz ['bora', 'cem', 'ece']
ece ['deniz', 'fuat']
fuat ['ece']
```

| İş | Kenar listesi | Komşuluk sözlüğü (küme) | Komşuluk matrisi |
|---|---|---|---|
| `a` ile `b` komşu mu? | `O(m)` | ortalama `O(1)` | `O(1)` |
| `a`'nın bütün komşuları | `O(m)` | `O(derece)` | `O(n)` |
| Bellek | `O(m)` | `O(n + m)` | `O(n²)` |

`n` düğüm, `m` kenar sayısı. Gerçek ağlar **seyrek (sparse)**: herkes herkesle
bağlı değil. 10 000 düğümlü, 50 000 kenarlı rastgele bir ağda:

```text
adjacency matrix cells : 100000000 (100 MB even at 1 byte each)
adjacency dict entries : 100000
```

Matris kenarlardan bin kat fazla hücre tutuyor ve neredeyse hepsi 0.
Seyrek graflarda komşuluk sözlüğü, küçük ve yoğun graflarda matris.

## Derece ve en bağlantılı düğüm

```python
degree = {node: len(neighbours) for node, neighbours in graph.items()}
print(sorted(degree.items(), key=lambda kv: (-kv[1], kv[0])))
```

```text
[('bora', 3), ('cem', 3), ('deniz', 3), ('ada', 2), ('ece', 2), ('fuat', 1)]
```

Sosyal ağ analizinde derece en basit **merkezilik (centrality)** ölçüsü:
çok bağlantısı olan kişi bilgiyi hızla yayar. Daha incelikli ölçüler
(PageRank) ML Algoritmaları modülünde.

## Arkadaş önerisi: ortak komşular

"Tanıyor olabileceğin kişiler" önerisinin en basit hâli: arkadaşlarının
arkadaşlarından, henüz arkadaşın olmayanları **ortak arkadaş sayısına** göre
sırala.

```python
def recommend(graph, person):
    scores = {}
    for friend in graph[person]:
        for other in graph[friend]:
            if other != person and other not in graph[person]:
                scores[other] = scores.get(other, 0) + 1
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))

print(recommend(graph, "ada"), recommend(graph, "ece"))

def jaccard(a, b):                       # ortak / toplam komşu
    return len(graph[a] & graph[b]) / len(graph[a] | graph[b])

print(round(jaccard("ada", "deniz"), 3))
```

```text
[('deniz', 2)] [('bora', 1), ('cem', 1)]
0.667
```

`ada`'ya `deniz` öneriliyor: iki ortak arkadaş (`bora`, `cem`). **Jaccard
benzerliği** ortak komşu sayısını toplam komşu sayısına böler; çok arkadaşı
olan birinin her öneride öne çıkmasını engeller. Bu, makine öğrenmesinde
**bağlantı tahmini (link prediction)** denen işin en basit özelliği.

## Matrisle saymak

Komşuluk matrisi NumPy ile cebir yapmaya izin verir. `A @ A` matrisinin
`[i][j]` hücresi, `i`'den `j`'ye **iki adımlık** yolların sayısıdır, yani
ortak komşu sayısı; köşegeni de derecedir.

```python
import numpy as np

names = sorted(graph)
index = {name: i for i, name in enumerate(names)}
A = np.zeros((len(names), len(names)), dtype=int)
for a, b in edges:
    A[index[a], index[b]] = A[index[b], index[a]] = 1

A2 = A @ A
print(A2[index["ada"], index["deniz"]], np.diag(A2).tolist())
```

```text
2 [2, 3, 3, 3, 2, 1]
```

`ada` ile `deniz` arasında 2 ortak komşu, sözlükle bulduğumuzun aynısı.
`A`'nın kuvvetleri (`A³`, `A⁴`…) daha uzun yolları sayar; graf sinir ağları
(GNN) da komşuluk matrisiyle bu tür çarpımlar yapar.

## Özet

- Graf: düğümler ve kenarlar; yönlü ya da yönsüz, ağırlıklı ya da değil.
- Komşuluk sözlüğü (seyrek graflar), matris (küçük ve yoğun graflar), kenar
  listesi (saklamak için).
- Derece: en basit merkezilik.
- Ortak komşu ve Jaccard: arkadaş önerisi, bağlantı tahmini.
- `A @ A`: iki adımlık yolların sayısı.
- Sıradaki bölüm: graf üzerinde gezinmek (BFS, DFS).
