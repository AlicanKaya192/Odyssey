## Terms

| Term | Meaning |
|---|---|
| Node (vertex) | a point of the graph: a person, a city, a page |
| Edge | the link between two nodes |
| Neighbour | a node directly connected by an edge |
| Degree | the number of edges of a node; in and out are separate when directed |
| Directed / undirected | whether an edge goes one way |
| Weighted | an edge has a value (length, time) |
| Path | a sequence of nodes joined by edges |
| Cycle | a path that returns to its starting node |
| Connected | there is a path from every node to every node |
| Sparse / dense | the number of edges is far below / close to `n²` |

## Building patterns

```python
graph = {}
for a, b in edges:                        # undirected
    graph.setdefault(a, set()).add(b)
    graph.setdefault(b, set()).add(a)

directed = {}
for a, b in edges:                        # directed: only a → b
    directed.setdefault(a, set()).add(b)
    directed.setdefault(b, set())         # so a node with no exits shows up too
```

In a weighted graph use a dictionary instead of a set: `graph[a][b] = weight`.

## Which representation?

- **Adjacency dictionary:** the default choice; sparse graphs, traversal
  algorithms.
- **Matrix:** small and dense graphs, algebra like `A @ A`, or when "is there
  an edge?" is asked very often.
- **Edge list:** storing in a file, sorting edges by weight (Kruskal in
  minimum spanning trees).

## Ready-made packages

`networkx` gives graphs and hundreds of algorithms ready-made; for large
graphs `scipy.sparse` matrices fit a sparse adjacency matrix in memory. On
this path we write the algorithms ourselves; in real work you look at these
first.

## Common mistakes

- Adding an edge only one way in an undirected graph.
- Keeping only the nodes that appear in edges: a node with no edges does not
  show up in the dictionary; add it separately if needed.
- Keeping a large sparse graph in a dense matrix: 10,000 nodes are 100
  million cells.
