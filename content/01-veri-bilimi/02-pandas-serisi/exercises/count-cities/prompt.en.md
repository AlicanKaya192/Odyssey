You have the city of six records. When you open a dataset for the first
time, this is the first question you ask a categorical column: **how many of
each?**

**What you need to do:**

1. The `cities` Series is ready in the starter code.
2. Compute how many of each city there are into a Series called `counts`.
3. Print, in order: `counts`, how many **distinct** cities there are, and the
   name of the **most frequent** one.

**Expected output:**

```
Ankara    3
Izmir     2
Bursa     1
Name: count, dtype: int64
3
Ankara
```

The `Name: count` line is information pandas adds itself, saying what the
result is. You do not write it.
