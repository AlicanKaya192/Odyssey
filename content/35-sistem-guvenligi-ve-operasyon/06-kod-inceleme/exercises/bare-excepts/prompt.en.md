`bare_excepts(source)` should return the line number of every `except:`
block with no type written, as a list from smallest to largest. Catches
with a type (`except FileNotFoundError:`) do not count. In the AST an
untyped catch is an `ast.ExceptHandler` whose `type` field is `None`.

**Expected output:**

```
[4, 12]
```
