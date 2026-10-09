In recursive DFS Python keeps the call stack, and its depth is limited to
about 1000. If we do the same work with our own stack there is no limit:

```python
def dfs_stack(graph, start):
    order, seen, stack = [], set(), [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        for neighbour in sorted(graph[node], reverse=True):
            if neighbour not in seen:
                stack.append(neighbour)     # reversed: smaller names first
    return order

chain = {i: set() for i in range(5000)}     # 0 - 1 - 2 - ... - 4999
for i in range(4999):
    chain[i].add(i + 1)
    chain[i + 1].add(i)

order = dfs_stack(chain, 0)
print(len(order), order[:5], order[-1])

small = {"a": {"b", "c"}, "b": {"a", "d"}, "c": {"a"}, "d": {"b"}}
print(dfs_stack(small, "a"))
```

```text
5000 [0, 1, 2, 3, 4] 4999
['a', 'b', 'd', 'c']
```

The neighbours are pushed **in reverse order**; since the last one in comes
out first, the walk goes in the same (alphabetical) order as recursive DFS. A
node can enter the stack more than once; the `seen` check when it comes out
stops it from being handled twice.
