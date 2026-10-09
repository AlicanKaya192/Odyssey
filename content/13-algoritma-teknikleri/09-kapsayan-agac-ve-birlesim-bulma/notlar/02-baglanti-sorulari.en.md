Union-find is not only for Kruskal. When edges **arrive one by one**, it
answers "how many groups are there?" and "did this edge close a cycle?"
without walking the graph from scratch each time.

```python
parent = list(range(6))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

groups = 6
for a, b in [(0, 1), (2, 3), (1, 2), (4, 5), (0, 3)]:
    ra, rb = find(a), find(b)
    if ra == rb:
        print(a, b, "-> cycle!")
    else:
        parent[ra] = rb
        groups -= 1
        print(a, b, "-> groups:", groups)
```

```text
0 1 -> groups: 5
2 3 -> groups: 4
1 2 -> groups: 3
4 5 -> groups: 2
0 3 -> cycle!
```

Each new link that merges two groups lowers the group count by one; when
`0`–`3` arrived, both were already in the same group, so this edge closed a
cycle. Asking the same questions again with BFS on every edge costs
`O(n + m)`; here each edge takes constant time in practice.

The same pattern is used for: friend circles in a social network, islands on a
map, merging accounts of the same person (shared e-mail or phone), building
"same entity" groups in entity resolution.
