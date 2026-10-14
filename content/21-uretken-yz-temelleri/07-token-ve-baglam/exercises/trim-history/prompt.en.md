`trim(messages, budget)` should always keep the first message (the system
message) and drop the **oldest** message after it until
`count_message_tokens` no longer exceeds the budget. Return
`[number of messages left, number of tokens left]`. If it fits without
dropping anything, leave the list as it is.

**Expected output:**

```
[4, 53]
[6, 73]
```
