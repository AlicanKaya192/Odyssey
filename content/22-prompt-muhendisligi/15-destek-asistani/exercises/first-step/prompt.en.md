`first_step(message)` should make the decision before the model is called:
if the message matches the given `DETECT` pattern, `["blocked", None]`;
otherwise `["model", order number]` (the first match of the given
`ORDER_ID`, or `None` if there is none).

**Expected output:**

```
['model', 'ORD-48213']
['blocked', None]
['model', None]
```
