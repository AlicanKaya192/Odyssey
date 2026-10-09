Write the function `append_value(head, value)`: it adds a new node with value
`value` at **the end** of the list and returns the head of the list.

There are two cases: if the list is empty, the new node becomes the head.
Otherwise go to the last node (the one whose `next` is `None`) and link the new
node to its `next`.

**Expected output:**

```
[1, 2, 3, 4]
[9]
```
