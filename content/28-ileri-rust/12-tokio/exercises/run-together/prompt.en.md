The code runs three jobs in order and takes about 600 ms. Run them together with `tokio::join!` so that it stays under 500 ms.

**Expected output:**

```text
2 4 6
fast: true
```
