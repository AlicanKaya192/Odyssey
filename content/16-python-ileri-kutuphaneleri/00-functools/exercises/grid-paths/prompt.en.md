The function `grid_paths(rows, cols)` counts recursively how many
different paths there are from the top left to the bottom right of a grid
of `rows` × `cols` cells, moving only right and down. The code is correct,
but at `16 × 16` it repeats the same computation millions of times and runs
out of time. Speed it up by adding **`@lru_cache`** to the function.

**Expected output:**

```
6
155117520
```
