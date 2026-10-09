Write a `Point` class: it holds `x` and `y`; **two points with the same
contents must count as equal** and be a single element in a set. Write
`__eq__` and `__hash__` for that (use the tuple `(x, y)` for the hash).

Then write the function `count_unique(pairs)`: it builds `Point` objects from
`[x, y]` pairs, puts them in a set and returns the set's size.

**Expected output:**

```
2
0
True
```

Without `__hash__`, identical points would be counted separately in the set.
