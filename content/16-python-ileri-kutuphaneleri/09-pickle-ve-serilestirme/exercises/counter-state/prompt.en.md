The `Counter` class holds a `threading.Lock` and therefore cannot be
pickled. Add `__getstate__` (a copy of the attributes without `lock`) and
`__setstate__` (put the state back, rebuild `lock`) to the class. The code at
the bottom round-trips the counter and adds once more.

**Expected output:**

```
3 lock
```
