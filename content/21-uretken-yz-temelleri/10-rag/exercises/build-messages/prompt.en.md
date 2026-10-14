`build_messages(question, texts)` should return two messages: first
`{"role": "system", "content": SYSTEM}`, then the user message. The user
message's content is: a `"Sources:"` line, a `"[n] text"` line for every chunk
(`n` starts at 1), an empty line and `"Question: question"`. The lines are
joined with `\n`.

**Expected output:**

```
Sources:
[1] Gift cards are valid for 3 years.
[2] Points expire.

Question: Do gift cards expire?
```
