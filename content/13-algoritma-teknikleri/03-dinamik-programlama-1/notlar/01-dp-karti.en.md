## The recipe

1. **State:** what does a cell of the table mean?
2. **Transition:** how is a cell computed from smaller cells?
3. **Base:** the value of the smallest cells.
4. **Order:** so that the needed cells are filled first.
5. **Answer:** which cell?

## Top-down or bottom-up?

| | Memoization | Tabulation |
|---|---|---|
| Writing it | add a dictionary or `@cache` to the recursive solution | you have to think about the order |
| Computed | only the subproblems that are needed | the whole table |
| Depth | can hit the recursion limit | no problem |
| Shrinking memory | hard | easy (only the last rows) |

The depth limit is a real problem:

```python
from functools import cache

@cache
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)

try:
    fib_memo(5000)
except RecursionError:
    print("RecursionError")

def fib_table(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(len(str(fib_table(5000))), "digits")
```

```text
RecursionError
1045 digits
```

## Common shapes

| Shape | Example | State |
|---|---|---|
| One dimension, the previous few cells | Fibonacci, stairs | `dp[i]` |
| One dimension, every option | the fewest coins | `dp[amount]` |
| One pass, "ending here" | Kadane | `current` |
| Two dimensions, above and left | paths on a grid | `dp[r][c]` |
| Two sequences | longest common subsequence, edit distance | `dp[i][j]` (DP 2) |
| Item × capacity | 0/1 knapsack | `dp[i][w]` (DP 2) |

## Common mistakes

- Setting the base case wrong: `ways[0] = 1` in the how-many-ways question
  (giving no coins is one way), `best[0] = 0` in the fewest-coins question.
- Mixing up the loop order in the how-many-ways question: coins outside →
  combinations, amounts outside → orderings.
- Thinking an unreachable state is 0: in the fewest-coins question the start
  value is `inf`; if it is still `inf` at the end, that amount cannot be
  given.
- Passing a list as an argument with `@cache`: a list cannot be hashed,
  `TypeError`; pass a tuple.
