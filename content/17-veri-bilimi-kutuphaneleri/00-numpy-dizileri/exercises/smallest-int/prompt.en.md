`smallest_int(values)` should try the types `int8`, `int16`, `int32`,
`int64` in order with `np.iinfo` and return, as text, the name of the
**first** type that both the smallest and the largest value of the list fit
into (like `"int8"`; `np.dtype(kind).name`).

**Expected output:**

```
int8 int16 int32
```
