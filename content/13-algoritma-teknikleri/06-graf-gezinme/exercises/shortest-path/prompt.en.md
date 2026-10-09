Write the function `shortest_path(edges, start, goal)`: with BFS it returns
the path with the fewest steps as a list of nodes; `None` if there is no path.
Look at the neighbours **in alphabetical order** (which of several equally
long paths is chosen depends on it).

Keep each node's parent in a `parent` dictionary; walk back from the goal and
reverse the list.

**Expected output:**

```
['ada', 'bora', 'deniz', 'ece', 'fuat']
['cem', 'deniz', 'ece']
None
```
