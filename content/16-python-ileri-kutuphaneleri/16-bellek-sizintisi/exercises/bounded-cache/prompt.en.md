`BoundedCache` grows without limit. Turn it into an LRU cache that keeps at
most `max_size` items using `OrderedDict`:

- `put`: add, move it to the end with `move_to_end(key)`; if the limit is
  exceeded, drop the oldest with `popitem(last=False)`.
- `get`: `None` if missing; otherwise move it to the end and return the value.

`simulate` is ready; it returns the keys left in the cache in order.

**Expected output:**

```
['c', 'a', 'd']
['y', 'z']
```
