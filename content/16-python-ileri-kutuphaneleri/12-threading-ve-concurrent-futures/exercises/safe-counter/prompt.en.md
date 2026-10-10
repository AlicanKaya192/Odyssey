`Counter.add_many(n)` increases the value `n` times; when four threads
increase the same counter 500 times each it should be 2000, but increments
get lost. Create a `threading.Lock()` in `__init__` and put the read-write
step inside a `with self.lock:` block.

**Expected output:**

```
2000
```
