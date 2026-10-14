`fixed_share(system, inputs)` should find the token count of the message
list `[system, user]` for each input with `count_message_tokens`. Return
`[total tokens of all calls, total tokens of the system message content
over all calls, the second divided by the first]`; the share rounded to 2
places (`0.0` if `inputs` is empty).

**Expected output:**

```
[40, 12, 0.3]
[62, 34, 0.55]
```
