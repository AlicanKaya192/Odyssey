## Types

| dtype | Bytes | Range / precision |
|---|---|---|
| `int8` / `uint8` | 1 | −128…127 / 0…255 |
| `int16` | 2 | −32,768…32,767 |
| `int32` | 4 | ±2.1 billion |
| `int64` | 8 | ±9.2 × 10¹⁸ (the default integer) |
| `float32` | 4 | ~7 significant digits |
| `float64` | 8 | ~16 significant digits (the default decimal) |
| `bool` | 1 | `True` / `False` |
| `<U10` | 40 | text of at most 10 characters (4 bytes per character) |
| `object` | 8 + the object | a Python object; slow |

## Tools

| Code | What it does |
|---|---|
| `a.dtype`, `a.itemsize`, `a.nbytes` | type, item size, total size |
| `np.iinfo(np.int16)` / `np.finfo(np.float32)` | limits |
| `a.astype(np.int32)` | change the type (a new array; silently breaks what overflows) |
| `np.result_type(a, b)` | which type an operation's result has |
| `np.shares_memory(a, b)` | do they share the same memory? |
| `a.ravel()` / `a.flatten()` | a view (when possible) / a copy |
| `np.linspace(0, 1, 5)` | equal steps with the stop included |

## Silent errors

| Symptom | Cause |
|---|---|
| `-56` instead of `200` | `int8` overflowed |
| `44` instead of `300` | `astype(np.int8)` |
| `16777216` instead of `16777217` | `float32` precision |
| `"hel"` instead of `"hello"` | a fixed-width text array |
| `<U32` in a number array | a string mixed in |
| `object` dtype | `None` or mixed objects |
