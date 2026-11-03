A frame is a list of numbers: first a buffer of `size` numbers, then
right after it the canary. `canary_intact(frame, size, canary)` should
return whether the canary is intact. If the frame is too short to hold the
canary (there is no index `size`), it should return `False`; it must not
raise an error.

**Expected output:**

```
True
False
False
```
