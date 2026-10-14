`build_messages(system, examples, text)` should return this list: first the
`system` message; then for each `[text, label]` pair in `examples` a
`user` message (the text) and an `assistant` message (the label); last a
`user` message with the content `text`.

**Expected output:**

```
6
['user', 'assistant', 'user']
warranty
```
