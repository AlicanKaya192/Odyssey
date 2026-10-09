Write the function `reverse(head)`: it reverses the linked list **in place**
(without building new nodes, by turning the links) and returns the new head.

Three pointers: `prev`, `head`, `nxt`. The order: save the next one, turn the
arrow back, step forward. No `reversed` and no converting to a Python list.

**Expected output:**

```
[4, 3, 2, 1]
[]
```
