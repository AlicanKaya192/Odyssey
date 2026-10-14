`retry(spec, attempts, window)` should call the script built by the given
`make_script` (`"429"` and `"503"` are errors, the rest are answers) with
`ChatClient(..., context_window=window)` (`MESSAGES`, `max_tokens=40`).
On a temporary error it should add a wait of `2.0 ** attempt` seconds to
the list and try again; return `[answer, waits]`. When the attempts run
out, `["gave up", waits]`; on `ContextLengthError` at once `["too long",
waits]`.

**Expected output:**

```
['ok', [1.0, 2.0]]
['gave up', [1.0, 2.0]]
['too long', []]
```
