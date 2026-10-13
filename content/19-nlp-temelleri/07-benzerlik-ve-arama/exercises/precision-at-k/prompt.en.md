`precision_at_k(k)` should rank the articles by score for each ticket and
return, with 3 places, the share of tickets where at least one of the first
`k` articles has the ticket's category. The similarity table `S` is ready
(rows are tickets, columns articles).

**Expected output:**

```
1 0.809
2 0.885
3 0.934
```
