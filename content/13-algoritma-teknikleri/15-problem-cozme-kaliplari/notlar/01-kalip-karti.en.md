## While solving a problem

1. **Understand:** what is the input, what is the output? Say it in one
   sentence in your own words.
2. **Solve two or three examples by hand,** one of them an edge case (empty,
   one item, all equal).
3. **Estimate the budget:** how large can `n` be? Which complexity fits?
4. **Brute force first:** a slow but correct solution. Sometimes it is enough;
   if not, you need it for stress testing.
5. **Look for the pattern:** what are you computing again and again? Would
   sorting, hashing, a stack, binary search or DP help?
6. **Test:** edge cases and random inputs against brute force.

## Costs of the patterns

| Pattern | Cost | Precondition |
|---|---|---|
| Binary search on the answer | `O(check × log range)` | a one-directional check |
| Monotonic stack | `O(n)` | each item enters once and leaves once |
| BFS in a state space | `O(states + moves)` | a reasonable number of states |
| Meet in the middle | `O(2^(n/2) · n)` | the problem can be split in two |

## Common mistakes

- Rushing to the most complex solution without looking at the budget: if
  `n = 15`, brute force is enough.
- Setting the range wrong in binary search on the answer: the lower bound is
  the largest box (`max`), the upper bound is all of them (`sum`); a capacity
  below `max` is never enough.
- Not thinking about `<` versus `<=` in a monotonic stack: equal values.
- Forgetting to mark visited states in BFS: the same state enters the queue
  endlessly.
