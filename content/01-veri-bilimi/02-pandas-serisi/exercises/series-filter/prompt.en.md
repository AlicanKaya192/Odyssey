The prices of five products sit in a Series with their names. You will
separate the expensive ones.

**What you need to do:**

1. The `prices` Series is ready in the starter code.
2. Collect the ones priced **100 or above** into a Series called
   `expensive`.
3. Print, in order: `expensive`, how many products there are, and the average
   price (rounded to one place).

**Expected output:**

```
kalem    120
canta    240
kitap    175
dtype: int64
3
178.3
```

**Notice:** in NumPy, filtering left you with only the numbers. Here the
**product names come along** — you do not lose which price belongs to which
product. This is exactly what a Series' index is for.
