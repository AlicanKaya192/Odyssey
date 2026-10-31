Write the `JoinHandle` future and `spawn`. `spawn` awaits the given future inside `spawner.detach`, puts the result in the state, and wakes the waker if any.

**Expected output:**

```text
three 2
```
