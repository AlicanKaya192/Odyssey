`cache_run(requests)` should go over the requests. The key is the text in
lower case with its spaces simplified (`" ".join(text.lower().split())`).
If the key was seen before, count a hit and count that request's
`count_message_tokens(messages_for(text))` tokens as saved; otherwise one
model call. Return `[calls, hits, saved tokens]`.

**Expected output:**

```
[2, 2, 60]
[0, 0, 0]
```
