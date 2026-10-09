Write the function `max_subarray(values, lo=0, hi=None)` **with divide and
conquer**: it returns the sum of the maximum subarray (consecutive elements,
at least one element) of `values[lo..hi]`.

The answer is one of three: the left half's answer, the right half's answer,
the best sum crossing the middle (the best going left from the middle + the
best going right).

The 200,000-element input on the last line makes an `O(n²)` solution hit the
time limit.

**Expected output:**

```
7
-1
591
```
