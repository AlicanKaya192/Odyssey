Write the function `has_duplicate(items)` with nested loops: it compares
every pair (`i < j`) and returns the tuple `(found, comparisons)`.

- When it finds the first equal pair, return `(True, comparisons)`
  **at once**.
- If there is no equal pair, return `(False, comparisons)`.

**Expected output:**

```
(True, 1)
(True, 5)
(False, 4950)
```

With no repeat (the worst case) 100 elements need 4950 comparisons: every
pair. With the repeat at the start, a single comparison was enough.
