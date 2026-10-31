Write `send`, `Clone`, `Drop` and the `Recv` future. Keep the `senders` counter. When the last sender drops, wake the waiting receiver so it gets `None`.

**Expected output:**

```text
6
```
