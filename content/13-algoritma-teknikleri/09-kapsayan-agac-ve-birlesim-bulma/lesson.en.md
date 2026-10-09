# Spanning Trees and Union-Find

You will connect six cities with fibre cable. Each pair of cities has a
different cable cost, and reaching every city by one route is enough. Which
network is the cheapest? This is the **minimum spanning tree (MST)** problem:
the set of edges that connects all nodes, has no cycle and has the smallest
total weight.

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
<figcaption>Six cities, nine possible cables. The purple edges are the minimum spanning tree: five edges, total 14.</figcaption>
</figure>

A spanning tree with `n` nodes always has `n − 1` edges: with one edge fewer
the graph falls apart, with one edge more a cycle appears. Both methods in this
section (Kruskal and Prim) are **greedy**: at each step they take the cheapest
suitable edge, and both find the best tree.

## Union-find: who is in which group?

The only question Kruskal asks is: "Are the two ends of this edge already
connected?" If they are, the edge would make a cycle. Asking this by walking
the graph every time would be slow. The **union-find (disjoint set union,
DSU)** structure does two jobs very fast:

- `find(x)`: the **representative** (root) of `x`'s group.
- `union(a, b)`: merge two groups; `False` if they are already the same group.

Each item looks at a **parent**; the root is its own parent. Items that reach
the same root are in the same group.

```python
class DSU:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # shorten the path
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                       # already the same group
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                   # small group under the big one
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

`A` and `C` were never merged directly, but they are in the same group through
`B` and `D`. The last line is `False`: that edge would make a cycle.

## Two small tricks, a big difference

Two details make the structure fast:

- **Union by size:** the root of the smaller group goes under the bigger one;
  the tree does not get deep.
- **Path compression:** while `find` climbs, it moves the items it passes
  closer to the root; later queries get shorter.

Without them, when items are merged in order the tree turns into a long chain.
The code below merges `0`–`1`, `1`–`2`, ... then asks for the root of every
item and counts how many steps `find` climbs:

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
        parent[a] = b                  # a's root goes under b
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

Without the tricks the number of steps grows like `n²` (5 times the items, 25
times the steps); with them, like `n`. When both are used, the average cost of
an operation is constant in practice (the theoretical bound is `α(n)`, the
inverse Ackermann function; even for as many items as there are atoms in the
universe it does not exceed 5).

## Kruskal: edges from cheap to expensive

Sort the edges by weight. Look at each edge in order: if its two ends are in
different groups, take it into the tree and merge the groups; if they are in
the same group, skip it (it would make a cycle).

```python
edges = [(4, "A", "B"), (3, "A", "C"), (2, "B", "C"), (5, "B", "D"),
         (7, "C", "D"), (6, "C", "E"), (1, "D", "E"), (3, "D", "F"),
         (4, "E", "F")]                # (weight, end, end)


def kruskal(nodes, edges):
    dsu = DSU(nodes)
    tree = []
    for w, a, b in sorted(edges):
        if dsu.union(a, b):            # different groups: no cycle
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

The nine edges total 35, the tree 14. `A`–`B` (4) and `E`–`F` (4) were
skipped: when their turn came, their ends were already connected. The cost
comes from sorting: `O(m log m)`.

## Prim: grow the tree from one node

Prim starts from one node and at each step adds the cheapest edge **leaving the
tree**. A heap finds the cheapest edge: very similar to Dijkstra, but the
number in the heap is only the edge's weight, not the path's total.

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
            continue                   # both ends in the tree: a cycle
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

The edges came in a different order, but the tree and the total are the same:
14. Kruskal is convenient on sparse graphs when you have an edge list; Prim
works well with an adjacency list and on dense graphs.

## In machine learning: single-linkage clustering

If you **stop Kruskal early**, you have clustered. Sort all pairs of points by
distance and merge; stop when the number of groups drops to `k`. The remaining
groups are the result of **single-linkage hierarchical clustering**.

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

The group numbers differ (ours are the representatives' positions), but
`adjusted_rand_score` is 1.0: the **same** groups as scikit-learn. Single
linkage finds long, thin clusters well; a single bridge point between two
clusters, however, can merge them (the chaining effect).

## Summary

- Spanning tree: all nodes, `n − 1` edges, no cycle; the MST is the cheapest.
- Union-find: `find` and `union`; with union by size + path compression,
  constant time in practice.
- Kruskal: sort the edges, take the ones that make no cycle (`O(m log m)`).
- Prim: grow from one node, the cheapest leaving edge with a heap.
- Stopping Kruskal at `k` groups = single-linkage clustering.
