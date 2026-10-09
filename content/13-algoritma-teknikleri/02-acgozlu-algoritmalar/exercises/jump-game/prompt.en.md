Write the function `can_reach_end(jumps)`: `jumps[i]` is the most steps you can
jump forward from position `i`. Starting at position 0, it returns `True` if
you can reach the last position.

**Greedy:** keep the farthest position reachable so far (`farthest`). If a
position is beyond `farthest`, it can never be reached; otherwise
`farthest = max(farthest, i + jumps[i])`.

- `[2, 3, 1, 1, 4]` → `True`, `[3, 2, 1, 0, 4]` → `False`

The last line is a list of 300,000 positions; a solution that marks every
jump from every position hits the time limit.

**Expected output:**

```
True
False
True
```
