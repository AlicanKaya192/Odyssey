`mark_repeats(calls)` should write `"run"` or `"repeat"` for every tool
call: `"repeat"` if the same call (the same `json.dumps(call,
sort_keys=True)`) came before. A call with the same content but keys in a
different order is a repeat too.

**Expected output:**

```
['run', 'run', 'repeat', 'repeat']
```
