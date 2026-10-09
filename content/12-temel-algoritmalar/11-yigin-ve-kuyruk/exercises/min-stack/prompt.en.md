Write the `MinStack` class:

- `push(x)`: puts `x` on the stack.
- `pop()`: removes and returns the top value.
- `minimum()`: returns the smallest value in the stack **in `O(1)`** (without
  scanning the stack).

Next to each element, also store the smallest value at the moment it was
pushed: `(value, smallest_at_that_moment)` tuples.

**Expected output:**

```
2
2 3
7 3
```
