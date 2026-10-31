Write `#[derive(TypeName)]`: it produces `fn type_name() -> &'static str` for a struct or `enum`. The name is the token after the word `struct` or `enum`; `pub` may come before.

**Expected output:**

```text
Point
Color
```
