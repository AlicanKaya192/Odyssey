`run_exchange(p, g, a, b)` should simulate the two sides' key exchange and
return `[ada_public, can_public, ada_shared, can_shared]`. Each side
computes the shared secret from **the other side's** public value and
**its own** secret number. In the starter code each side uses its own
public value and the shared secrets do not match.

**Expected output:**

```
[8, 19, 2, 2]
True
```
