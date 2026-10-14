`system_with_memory(base, memory)` should return `base` if the memory is
empty; otherwise `base + " Known facts: "` followed by every `key=value`
pair in memory joined with `"; "` (in the dictionary's order).

**Expected output:**

```
Be brief. Known facts: name=Ada; order=ORD-1
Be brief.
```
