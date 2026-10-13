`dominant(weights, share)` should return the number of the heaviest topic for
each document row; but if that topic's weight is less than `share` of the
row total (or the row total is 0), write `-1` ("mixed").

**Expected output:**

```
[0, -1, -1]
```
