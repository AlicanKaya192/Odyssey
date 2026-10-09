Write the function `peak_index(values)`: the list first **strictly
increases**, then **strictly decreases** (a mountain shape; it may also be
only increasing or only decreasing). Find the **index** of the largest
element in `O(log n)`.

Hint: if `values[mid] < values[mid + 1]` you are walking uphill and the peak
is to the right; otherwise the peak is at `mid` or to its left.

The last line searches a list of a million elements 2000 times; a linear
scan hits the time limit. No `max` and no `index`.

**Expected output:**

```
2
2
1199998000
```
