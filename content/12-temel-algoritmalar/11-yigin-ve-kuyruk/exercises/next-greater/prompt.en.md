Write the function `next_greater(values)` **with a monotonic stack**: for each
element it returns the **first greater** value after it; `-1` if there is
none.

- `[2, 7, 3, 5, 4, 6, 8]` → `[7, 8, 5, 6, 6, 8, -1]`

Keep the **indices** of elements waiting for their answer on the stack. When a
new value arrives, it is the answer for all smaller values on top of the
stack.

**Speed requirement:** at the end of the code there are 200 000 decreasing
temperatures; a nested loop would take 20 billion steps and the time limit
(10 seconds) would not be enough.

**Expected output:**

```
[7, 8, 5, 6, 6, 8, -1]
200000
```
