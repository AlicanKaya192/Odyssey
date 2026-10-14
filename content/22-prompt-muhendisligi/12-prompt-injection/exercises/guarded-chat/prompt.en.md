`guarded(script, message)` should join three layers. If the message
matches the given `DETECT` pattern, `["blocked input", ""]` without
calling the model. Otherwise send `[system, user]` with
`ChatClient(script)` (`SYSTEM`, `max_tokens=80`). If the answer contains
`CANARY`, `["blocked output", "leak"]`; if a domain found by `LINK` is not
in `ALLOWED`, `["blocked output", domain]`; otherwise `["sent", answer]`.

**Expected output:**

```
['sent', 'It ships today.']
['blocked input', '']
['blocked output', 'evil.example']
['blocked output', 'leak']
```
