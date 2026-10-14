The starter's `run_tool` **crashes** on an unknown tool, a missing order
or a wrong argument. Fix it: if the tool is not in `TOOLS`,
`{"error": "unknown tool <name>"}`; if a `TypeError` or `KeyError` happens
while running, `{"error": "wrong arguments"}`; if the call has no
`arguments`, use an empty dictionary.

**Expected output:**

```
{'status': 'shipped'}
{'error': 'wrong arguments'}
{'error': 'wrong arguments'}
{'error': 'unknown tool refund'}
```
