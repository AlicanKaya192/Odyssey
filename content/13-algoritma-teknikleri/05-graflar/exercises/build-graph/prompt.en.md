Write the function `build_graph(edges)`: from `[a, b]` pairs it builds an
**undirected** adjacency dictionary (node → set of neighbours). Add each edge
**both ways**; `setdefault` makes it easy.

`neighbours(edges)` turns the result into sorted lists so it can be
compared.

**Expected output:**

```
ada ['bora', 'cem']
bora ['ada', 'cem', 'deniz']
cem ['ada', 'bora', 'deniz']
deniz ['bora', 'cem', 'ece']
ece ['deniz', 'fuat']
fuat ['ece']
```
