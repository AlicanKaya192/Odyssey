`window(history, keep)` should always keep the history's first message
(the system message) and then add only the last `keep` messages. If
`keep` is larger than the number of remaining messages, all of them
come.

**Expected output:**

```
['S', 'm3', 'm4', 'm5']
['S', 'm0', 'm1', 'm2', 'm3', 'm4', 'm5']
```
