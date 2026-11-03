`k_anonymity(rows, quasi)` should group the rows by the values of the
fields in `quasi` (a tuple of those fields for each row) and return the
size of the smallest group. With no rows, `0`. If `quasi` is empty, all
rows form one group.

**Expected output:**

```
1
1
5
```
