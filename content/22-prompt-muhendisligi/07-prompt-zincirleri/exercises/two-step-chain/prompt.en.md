`two_steps(script, message)` should run two steps with
`ChatClient(script)`. Step one: send the `CLASSIFY` instruction with the
given `ask` and read the answer as JSON; if the category is not in
`POLICY` (or it is not JSON), return `[["classify", False], None]`. Step
two: send the same message with the instruction
`"Answer using only this policy: " + POLICY[category]` and return
`[["classify", True], answer]`.

**Expected output:**

```
True It arrives in 3 to 5 days.
False None
False None
```
