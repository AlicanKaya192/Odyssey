`split_sets(tickets, per_label)` should go through the messages in order:
the `"id"` of the first `per_label` messages of each category (`"label"`)
goes to the development list, the rest to the test list. Return
`[development, test]`.

**Expected output:**

```
20 20
[1, 2, 3, 4, 5, 6]
[21, 22, 23, 24, 25, 26]
```
