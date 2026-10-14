`assistant(script, message)` should build the path from the lesson (no
retries). If the message matches `DETECT`, `["blocked", ""]`. Otherwise
classify with `ChatClient(script)` (`[system "Answer with one category
word.", user]`, `max_tokens=20`, `parse_label`). If there is no category or
it is in `TO_PEOPLE`, `["handover", ""]`. Find the order data with
`get_order`, ask for an answer with `SYSTEM` and
`f"Order data: {data}\n\nCustomer: {message}"` (`max_tokens=80`; `data`
is `"none"` without data). If the given `problems` is true,
`["handover", answer]`, otherwise `["sent", answer]`.

**Expected output:**

```
sent
blocked
handover
handover
```
