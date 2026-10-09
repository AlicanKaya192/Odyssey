Write the function `common_elements(a, b)`: it returns the values that
occur in both lists, as a list **sorted from smallest to largest and without
repeats**.

- `[1, 2, 2, 3]` and `[2, 3, 4]` → `[2, 3]`

**Speed requirement:** at the end of the code two lists of 100 000 and
66 667 elements are compared, and the time limit is 10 seconds. A nested loop
is `O(n × m)`; turn one of the lists into a **set** and look the other's
elements up in it. You may use `sorted` to sort the result.

**Expected output:**

```
[2, 3]
33334
```
