`dispatch(call, confirmed)` should run the call according to the given
`TOOLS` dictionary: if the tool does not exist, `{"error": "unknown tool
<name>"}`; if the tool's `"confirm"` value is `True` and `confirmed` is
`False`, `{"pending": "needs the customer's confirmation"}`; otherwise run
the tool's function with the call's arguments and return the result.

**Expected output:**

```
['pending']
['cancelled', 'order_id']
['order_id', 'status']
```
