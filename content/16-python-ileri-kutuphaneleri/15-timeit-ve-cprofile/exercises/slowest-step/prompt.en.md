`slowest_step()` should profile `pipeline()` with `cProfile` and return the
name, among those in the `STEPS` list, with the **largest cumulative time
(cumtime)**. The fourth item (`[3]`) of a stats value is `cumtime`.

**Expected output:**

```
read
```
