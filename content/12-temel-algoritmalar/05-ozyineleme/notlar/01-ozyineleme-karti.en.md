## The pattern

```text
def solve(problem):
    if problem is in its smallest form:    # base case
        return the direct answer
    smaller = make the problem one step smaller
    answer_small = solve(smaller)          # call itself
    return build the bigger answer from answer_small
```

## Checklist

1. **Is there a base case?** An empty list, `n <= 1`, an empty string…
2. **Does every call get closer to the base case?** `n - 1`, `items[1:]`,
   `text[1:]`. Calling `solve(n)` from inside `solve(n)` is an endless loop.
3. **Is the result of the recursive call used?** The most common mistake:

   ```python
   def total(items):
       if not items:
           return 0
       items[0] + total(items[1:])     # return forgotten → returns None
   ```

4. **Does every path end with `return`?** Forgetting `return` in one `if`
   branch makes the function return `None` on that branch.

## Common patterns

| Problem | Base case | Step |
|---|---|---|
| `n!` | `n <= 1` → 1 | `n * f(n - 1)` |
| Sum of a list | empty → 0 | `items[0] + f(items[1:])` |
| Reversing a string | empty → `""` | `f(text[1:]) + text[0]` |
| Sum of digits | `n < 10` → `n` | `n % 10 + f(n // 10)` |
| Powers | `exp == 0` → 1 | `base * f(base, exp - 1)` |
| A nested list | element not a list → itself | `f(sub)` for every sublist |

## The mutable default value trap

When carrying an accumulator list through recursion, **do not make the
default value a list**:

```python
def collect(items, result=[]):     # wrong: the same list is shared by every call
    ...

def collect(items, result=None):   # right
    if result is None:
        result = []
    ...
```

The default value is built **once**, when the function is defined; on a
second call the first call's results are still in the list.
