`loop_steps(actions, max_steps)` should imitate an agent's rounds:
`actions` is what the model does in each round (`"tool"` or `"answer"`).
At most `max_steps` rounds are run; at the first `"answer"` round return
`[that round, True]`. If the limit is reached or the actions run out
before an answer, `[number of rounds run, False]`.

**Expected output:**

```
[3, True]
[5, False]
```
