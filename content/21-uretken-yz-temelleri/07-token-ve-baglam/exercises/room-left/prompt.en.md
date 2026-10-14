`room(messages, window)` should find the token count of the message list
with `count_message_tokens` from the read-only `llm_client.py` and return
`[input tokens, the most tokens left for the answer]`. The room left is
`window - input`, but it does not go below 0.

**Expected output:**

```
[14, 86]
[14, 0]
```
