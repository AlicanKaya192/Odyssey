`build_messages(role, task, fmt, text)` should return a list of two
messages: first a `system` message whose content is `role`, `task` and
`fmt` joined with a space between each; then a `user` message whose
content is `text`. Each message is a dictionary of the form
`{"role": ..., "content": ...}`.

**Expected output:**

```
2
Be a shop assistant. Classify. One word.
user Where is my parcel?
```
