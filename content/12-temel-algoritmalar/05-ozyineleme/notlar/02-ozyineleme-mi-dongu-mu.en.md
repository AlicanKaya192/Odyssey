Every recursive function can also be written as a loop, and every loop as
recursion. Which one to choose depends on the shape of the problem.

| | Recursion | Loop |
|---|---|---|
| Where it is natural | nested structures: trees, folders, nested lists; divide and conquer | flat sequences, counters, "do it n times" |
| Extra memory | one stack frame per level: `O(depth)` | usually `O(1)` |
| Limit in Python | depth ~1000 (`RecursionError`) | none |
| Readability | very short if the definition is recursive | clearer for flat work |

## Turning recursion into a loop: keep your own stack

The lesson's `deep_sum` can also be written as a loop with **our own stack**
(a list) instead of Python's call stack:

```python
def deep_sum_loop(items):
    total = 0
    stack = [items]                 # lists still to process
    while stack:
        current = stack.pop()
        for item in current:
            if isinstance(item, list):
                stack.append(item)  # to be processed later
            else:
                total += item
    return total

print(deep_sum_loop([1, [2, 3], [4, [5, [6]]]]))   # 21
```

This version does not hit the depth limit: for very deeply nested structures
(tens of thousands of levels) it is the safe way.

## About `sys.setrecursionlimit`

Raising the limit is possible (`sys.setrecursionlimit(10_000)`), but it is not
a reliable fix for work whose depth can be truly large: every level uses
memory, and the limit only changes where the error appears. If the depth can
be large, turning it into a loop is sturdier.

## Tail recursion

If the recursive call is the function's **last job** (like `return f(n - 1)`,
with no further work on the result), it is called tail recursion. Some
languages (like Scheme) turn it into a loop automatically and the stack does
not grow. **Python does not**: tail recursion piles up stack frames too.
