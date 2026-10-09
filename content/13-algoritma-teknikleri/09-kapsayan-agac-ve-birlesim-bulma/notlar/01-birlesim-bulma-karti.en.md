## Union-find

| Operation | What it does | Cost (with both tricks) |
|---|---|---|
| `find(x)` | gives the group's root | constant in practice |
| `union(a, b)` | merges two groups, `False` if the same | constant in practice |
| `find(a) == find(b)` | in the same group? | constant in practice |

- **Union by size:** the smaller group's root goes under the bigger one.
- **Path compression:** `find` moves the items it passes closer to the root.
- Union-find cannot **split** groups: deleting an edge is not supported.

## Kruskal or Prim?

| | Kruskal | Prim |
|---|---|---|
| Idea | cheap edge to expensive, take the ones with no cycle | grow from one node, the cheapest leaving edge |
| Structure | sorting + union-find | heap + adjacency list |
| Cost | `O(m log m)` | `O(m log n)` |
| Convenient for | an edge list, a sparse graph | an adjacency list, a dense graph |
| Disconnected graph | one tree per part (a forest) | only the part it started in |

With equal weights there can be more than one minimum tree; the **total** is
always the same.

## Where?

- Network design: cable, pipelines, power grids
- Single-linkage clustering (stopping Kruskal at `k` groups)
- Image segmentation: merging neighbouring pixels by their difference
- A quick lower bound and approximate solution for the travelling salesman
  problem

## Common mistakes

- Writing `parent[a] = b` directly instead of using `find`: the **roots** of
  `a` and `b` must be merged, not the items themselves.
- Forgetting to sort the edges in Kruskal: a tree is built but not the
  cheapest one.
- Not skipping an edge from the heap in Prim whose end is already in the tree:
  a cycle.
- Not checking that Kruskal returned fewer than `n − 1` edges on a
  disconnected graph.
