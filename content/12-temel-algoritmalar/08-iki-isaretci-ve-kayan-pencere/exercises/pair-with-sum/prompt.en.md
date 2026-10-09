Write the function `pair_with_sum(items, target)` **with two pointers**: in a
sorted list it returns two elements adding up to `target` as a `(smaller,
larger)` tuple; `None` if there is none.

The pointers may not use the same element twice (`left < right`).

**Speed requirement:** at the end of the code a sum that is **not** there is
searched for in a list of 200 000 elements; the time limit is 10 seconds. A
nested loop would try 20 billion pairs and not make it.

**Expected output:**

```
(1, 6)
None
None
```
