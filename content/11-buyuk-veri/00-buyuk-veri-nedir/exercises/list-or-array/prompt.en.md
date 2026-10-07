Store the same 100 000 decimal numbers in a Python list and in a NumPy
array; measure the size of both.

**What to do:**

1. Build the list `values = [i * 0.5 for i in range(100_000)]`.
2. Build the array `array = np.arange(100_000) * 0.5`.
3. Find the real size of the list in bytes: the list itself
   (`sys.getsizeof(values)`) **plus** the size of every number in it.
4. Find the size of the array with `array.nbytes`.
5. Print the two sizes in MB (one decimal) on one line, and below it how
   many times bigger the list is than the array (one decimal).

**Expected output:**

```
3.1 0.8
4.0
```

A float object is 24 bytes and its address 8; in the array every number is 8
bytes.
