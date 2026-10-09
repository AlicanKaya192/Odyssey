# Graph Traversal

In the Trees section we saw two walks: **breadth-first (BFS)** with a queue
and **depth-first (DFS)** with a stack or recursion. In graphs both work the
same, with one difference: a graph can have **cycles**. On a path that loops
back like `ada → bora → cem → ada`, if you do not keep track of where you have
been, you go round forever. That is why every graph traversal has a set of
**visited** nodes.

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
<figcaption>This section's graph: two separate pieces. ada → bora → cem → ada is a cycle; gul and hakan are a separate component.</figcaption>
</figure>

```python
edges = [("ada", "bora"), ("ada", "cem"), ("bora", "cem"), ("bora", "deniz"),
         ("cem", "deniz"), ("deniz", "ece"), ("ece", "fuat"), ("gul", "hakan")]
graph = {}
for a, b in edges:
    graph.setdefault(a, set()).add(b)
    graph.setdefault(b, set()).add(a)
```

## BFS: the path with the fewest steps

BFS moves away from the start **level by level**: first what is reached in
one step, then in two steps… That is why in an unweighted graph **the first
path that reaches a node is the one with the fewest steps**.

```python
from collections import deque

def bfs_distances(graph, start):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in sorted(graph[node]):
            if neighbour not in distance:         # first arrival = shortest
                distance[neighbour] = distance[node] + 1
                queue.append(neighbour)
    return distance

print(bfs_distances(graph, "ada"))
```

```text
{'ada': 0, 'bora': 1, 'cem': 1, 'deniz': 2, 'ece': 3, 'fuat': 4}
```

The `distance` dictionary is also the visited set: once a node is in the
dictionary it never enters the queue again. Each node and each edge is handled
once: `O(n + m)`.

## Recovering the path

If the distance is not enough and you need the path itself, write down for
each node **where it came from** (its parent); then walk back from the goal.

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
        return None                               # unreachable
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

`gul` is in another piece: there is no path at all.

## DFS: go all the way down

DFS takes a path and goes as far as it can, then comes back. It is short to
write with recursion:

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

In this small graph the two orders came out the same, but the paths differ:
BFS reached `cem` directly from `ada` (1 step), while DFS first dived into
`bora` and came to `cem` from there (`ada → bora → cem`). Both walk every
reachable node in `O(n + m)`; the difference is the order. If you need **the
fewest steps**, BFS; for "is there a path?", finding cycles and ordering jobs,
usually DFS.

**Watch out:** recursive DFS hits Python's depth limit on a long chain:

```text
recursive DFS on a chain of 5000 nodes: RecursionError
```

On large graphs DFS is written without recursion too, with a stack (in the
note).

## Connected components

A graph can consist of several disconnected pieces. If we start a new walk
from every node not yet visited, each walk finds a **connected component**:

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

Connected components are often useful in data science: merging different
records of the same customer (records sharing the same e-mail or phone form a
component), fraud rings, disconnected communities in a social network.

## The shortest path on a grid

A maze is a graph too: each empty cell is a node, neighbouring cells are
edges. BFS finds the fewest steps to the exit.

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

## Summary

- A visited set is essential in graph traversal: cycles cause endless loops.
- BFS moves level by level with a queue; in an unweighted graph it finds the
  path with the fewest steps.
- For the path, keep each node's parent and walk back from the goal.
- DFS dives all the way down; its recursive form hits the limit on deep
  graphs.
- Each walk finds a connected component; record merging, communities.
- Grids and mazes are graphs too. All of it is `O(n + m)`.
