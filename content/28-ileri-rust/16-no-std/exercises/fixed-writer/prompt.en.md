Write `core::fmt::Write` for `Buffer`, returning `Err(fmt::Error)` for text that does not fit. `report`: writes the form `name=value` with `write!`.

**Expected output:**

```text
Ok(())
a=5
Err(Error)
true
```
