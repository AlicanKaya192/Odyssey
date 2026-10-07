The first step of parallel work is splitting the work into pieces. Write a
function that splits a range into equal pieces.

**What to do:**

Write the function `split_range(n, parts)`. It splits the range from 0 to `n`
into `parts` pieces and returns a list of `(start, stop)` tuples:

- The width of a piece is `size = n // parts`.
- Piece `i` is `(i * size, (i + 1) * size)`.
- **The last piece always stops at `n`**: if the division is not exact, the
  leftover is added to the last piece.

Examples:

- `split_range(100, 4)` → `[(0, 25), (25, 50), (50, 75), (75, 100)]`
- `split_range(10, 3)` → `[(0, 3), (3, 6), (6, 10)]`
