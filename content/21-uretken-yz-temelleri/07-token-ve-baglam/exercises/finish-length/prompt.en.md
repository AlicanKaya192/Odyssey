`ask_complete(start)` should ask the same question with
`ChatClient([ANSWER] * 5)` and the limit `max_tokens=start`. If the reply's
finish reason is `"length"`, double the limit and ask again; stop when
`"stop"` comes. Return `[text of the last reply, the last max_tokens used,
total number of calls]` (the number of calls is `len(client.calls)`).

**Expected output:**

```
5 20 3 True
40 40 1 True
```
