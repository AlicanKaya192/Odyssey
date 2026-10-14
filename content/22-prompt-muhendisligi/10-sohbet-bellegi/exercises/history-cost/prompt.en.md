`compare(questions, keep)` should imitate the conversation: add each
question to the history as a `user` message; in that round add up
separately with `count_message_tokens` the tokens sent with the whole
history (`[SYSTEM] + history`) and with only the last `keep` messages
(`[SYSTEM] + history[-keep:]`); then add `REPLY` as an `assistant`
message. Return `[whole history total, last messages total]`.

**Expected output:**

```
[337, 168]
[337, 337]
```
