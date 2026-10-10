`tag_counts(tags)` takes a list of texts, each with comma-separated tags
(`"gift,fast"`). It should return how many times each tag appears as `{tag:
count}`, sorted by tag name: `str.split(",")` → `explode` → `value_counts()`
→ `sort_index()`. **Do not write a loop.**

**Expected output:**

```
{'eco': 1, 'fast': 3, 'gift': 2}
```
