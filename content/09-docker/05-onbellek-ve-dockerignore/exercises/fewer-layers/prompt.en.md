Every `RUN` adds a layer to the image. Joining small, related steps into a
single `RUN` with `&&` reduces the number of layers.

**What to do:** join the three `RUN` lines into **one** `RUN` with `&&`.
Odyssey will check that the image has at most 2 layers (Alpine's own layer
+ yours).

**Expected output:**

```
alpha
beta
```
