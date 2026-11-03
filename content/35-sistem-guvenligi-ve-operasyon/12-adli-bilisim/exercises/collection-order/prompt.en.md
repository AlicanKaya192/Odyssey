Each source is `[name, volatility]`; a smaller number is more volatile.
`collection_order(sources)` should return the source names in collection
order: the most volatile first; within the same volatility, alphabetical
by name.

**Expected output:**

```
memory
connections
processes
disk
backup tapes
```
