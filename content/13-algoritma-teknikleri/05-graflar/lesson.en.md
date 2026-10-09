# Graphs

In a tree every node had a single parent. Most relationships in the real
world are not like that: in a social network everyone is friends with many
people, at a road junction many roads meet, web pages link to each other.
This structure is called a **graph**: **nodes (vertices)** and the **edges**
that connect them.

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
<figcaption>A friendship network of six people. deniz, with the green ring, is not ada's friend, but they have two friends in common.</figcaption>
</figure>

## Terms

- **Neighbour:** a node directly connected by an edge. The neighbours of `cem`
  are `ada`, `bora`, `deniz`.
- **Degree:** the number of edges of a node. The number of friends in a social
  network.
- **Undirected / directed:** friendship goes both ways (undirected);
  **following** an account or **linking** to a page goes one way (directed).
  In a directed graph the **in** and **out** degrees are separate.
- **Weighted:** an edge has a value (road length, time, cost).
- **Path:** a sequence of nodes joined by edges. `ada → cem → deniz`.
- **Connected:** a graph is connected if there is a path from every node to
  every node.

A tree is really a connected graph with no cycles.

## Putting a graph into code

There are three ways:

- **Edge list:** `[("ada", "bora"), ...]`. Natural for storing in a file and
  reading from somewhere.
- **Adjacency list:** for each node, the list or set of its neighbours. A
  dictionary in Python. The most used.
- **Adjacency matrix:** an `n × n` table; `A[i][j] = 1` if there is an edge
  between `i` and `j`.

```python
edges = [("ada", "bora"), ("ada", "cem"), ("bora", "cem"), ("bora", "deniz"),
         ("cem", "deniz"), ("deniz", "ece"), ("ece", "fuat")]

graph = {}
for a, b in edges:                       # undirected: add both ways
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

| Job | Edge list | Adjacency dictionary (sets) | Adjacency matrix |
|---|---|---|---|
| Are `a` and `b` neighbours? | `O(m)` | `O(1)` on average | `O(1)` |
| All neighbours of `a` | `O(m)` | `O(degree)` | `O(n)` |
| Memory | `O(m)` | `O(n + m)` | `O(n²)` |

`n` is the number of nodes, `m` the number of edges. Real networks are
**sparse**: not everyone is connected to everyone. On a random network with
10,000 nodes and 50,000 edges:

```text
adjacency matrix cells : 100000000 (100 MB even at 1 byte each)
adjacency dict entries : 100000
```

The matrix holds a thousand times more cells than there are edges, and almost
all of them are 0. Use an adjacency dictionary for sparse graphs, a matrix for
small and dense ones.

## Degree and the most connected node

```python
degree = {node: len(neighbours) for node, neighbours in graph.items()}
print(sorted(degree.items(), key=lambda kv: (-kv[1], kv[0])))
```

```text
[('bora', 3), ('cem', 3), ('deniz', 3), ('ada', 2), ('ece', 2), ('fuat', 1)]
```

In social network analysis degree is the simplest **centrality** measure: a
person with many connections spreads information quickly. Subtler measures
(PageRank) are in ALG 3.

## Friend suggestions: common neighbours

The simplest form of "people you may know": among your friends' friends, sort
those who are not yet your friends by **the number of common friends**.

```python
def recommend(graph, person):
    scores = {}
    for friend in graph[person]:
        for other in graph[friend]:
            if other != person and other not in graph[person]:
                scores[other] = scores.get(other, 0) + 1
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))

print(recommend(graph, "ada"), recommend(graph, "ece"))

def jaccard(a, b):                       # common / total neighbours
    return len(graph[a] & graph[b]) / len(graph[a] | graph[b])

print(round(jaccard("ada", "deniz"), 3))
```

```text
[('deniz', 2)] [('bora', 1), ('cem', 1)]
0.667
```

`deniz` is suggested to `ada`: two common friends (`bora`, `cem`). **Jaccard
similarity** divides the number of common neighbours by the total number of
neighbours; it stops someone with many friends from coming first in every
suggestion. This is the simplest feature of what machine learning calls
**link prediction**.

## Counting with the matrix

The adjacency matrix allows algebra with NumPy. The `[i][j]` cell of `A @ A`
is the number of **two-step** paths from `i` to `j`, that is the number of
common neighbours; its diagonal is the degree.

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

2 common neighbours between `ada` and `deniz`, the same as we found with the
dictionary. The powers of `A` (`A³`, `A⁴`…) count longer paths; graph neural
networks (GNNs) also do this kind of multiplication with the adjacency
matrix.

## Summary

- A graph: nodes and edges; directed or undirected, weighted or not.
- Adjacency dictionary (sparse graphs), matrix (small and dense graphs), edge
  list (for storing).
- Degree: the simplest centrality.
- Common neighbours and Jaccard: friend suggestions, link prediction.
- `A @ A`: the number of two-step paths.
- Next section: walking a graph (BFS, DFS).
