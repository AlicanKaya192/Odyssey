Write the `LRUCache` class with `collections.OrderedDict`:

- `LRUCache(capacity)`: holds at most `capacity` keys.
- `get(key)`: returns the value (`None` if missing) and makes the key **the
  newest**.
- `put(key, value)`: writes the value and makes the key the newest; if the
  capacity is exceeded, drops **the oldest**.

`move_to_end(key)` makes it the newest, `popitem(last=False)` drops the
oldest.

**Expected output:**

```
1
None 1 3
```
