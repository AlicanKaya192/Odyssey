A tuple is a list that cannot be changed. It is used to hold a fixed number of
values that belong together — a point, or a name-and-grade pair.

**What you need to do:**

1. Define a **tuple** called `point`: `(3, 7)`
2. Unpack the tuple into variables `x` and `y` on one line.
3. Define a list called `pairs` where each element is a name-and-grade
   **tuple**:

```python
[("Ada", 90), ("Brian", 40), ("Grace", 75)]
```

4. In a variable called `names`, hold just the names as a list.
5. In a variable called `best`, hold the **tuple** of the person with the
   highest grade.
6. Print `point`, `x`, `y`, `names` and `best` in that order.

**Expected output:**

```
(3, 7)
3
7
['Ada', 'Brian', 'Grace']
('Ada', 90)
```

Note: `best` is a tuple, not just the name — it appears in brackets in the
output.

> Unpacking a tuple: `x, y = point`. To find the highest, loop over the tuples
> and compare the grade; the second element of a tuple is `pair[1]`.
