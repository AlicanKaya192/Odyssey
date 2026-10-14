`feedback(errors)` should build the message for the model from the error
list: `"Your answer was not valid: "` + the errors joined with `"; "` +
`". Reply with the JSON object only."`. If the list is empty, return an
empty text.

**Expected output:**

```
Your answer was not valid: urgent must
be true or false. Reply with the JSON
object only.
''
```
