Write `#[derive(Show)]`: it produces `fn show(&self) -> String`, with a result like `Point { x: 1, y: 2 }` (values with `{:?}`). Find a field name as the name before a single `:`; do not be fooled by `::`.

**Expected output:**

```text
Point { x: 1, y: 2 }
User { name: "ada", age: 36, tags: [1, 2] }
```
