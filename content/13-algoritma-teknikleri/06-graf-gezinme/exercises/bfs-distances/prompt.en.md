Write the function `distances(edges, start)` **with BFS**: it returns the
dictionary that gives how many steps away each node reachable from `start` is.

The distance dictionary is also the visited set: write `distance + 1` for a
neighbour not in the dictionary and add it to the queue. `build_graph` is
ready.

**Expected output:**

```
ada 0
bora 1
cem 1
deniz 2
ece 3
fuat 4
{'gul': 0, 'hakan': 1}
```
