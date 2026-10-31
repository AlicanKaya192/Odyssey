Write `push`: if full, give the value back in `Err`. Write `pop`: `None` if empty, otherwise the last added. Do not allocate.

**Expected output:**

```text
None
Ok(())
Ok(())
Err("c")
Some("b")
Some("a")
None
```
