Four patterns; in all four the pointers **never go back**, so the total work
is `O(n)`.

## 1. Inwards from both ends (sorted list)

```text
left, right = 0, len(items) - 1
while left < right:
    if the condition holds:
        return ...
    if something bigger is needed:
        left += 1
    else:
        right -= 1
```

Examples: a pair adding up to `target`, a palindrome check (are the letters
at the two ends equal?), the two walls holding the most water.

## 2. Fast and slow (same direction)

```text
slow = 0
for fast in range(len(items)):
    if items[fast] is to be kept:
        items[slow] = items[fast]
        slow += 1
# items[:slow] is the result
```

Examples: removing repeats from a sorted list, moving zeros to the end,
deleting a given value; all in place, `O(1)` extra memory.

## 3. Fixed window

```text
total = sum(values[:k])
for i in range(k, len(values)):
    total += values[i] - values[i - k]     # in - out
```

Examples: a moving average, the largest `k`-day total, a threshold being
crossed within the last `k` events.

## 4. Variable window

```text
start = 0
for end in range(len(items)):
    add items[end] to the window
    while the window breaks the condition:
        remove items[start] from the window
        start += 1
    update the answer with end - start + 1
```

Examples: the longest piece without repeats, the shortest piece with a sum of
at least `target`, the longest piece with at most `k` distinct values.

## Check questions

- **Is it sorted?** If not, pointers from both ends work wrongly.
- **Can the values be negative?** In variable-window problems like "a sum of
  at least `target`", the assumption that shrinking the window lowers the sum
  only holds for **non-negative** numbers. With negatives you need prefix
  sums (the next section).
- **Empty input and `k > n`?** Decide what to return if no window can be
  built at all.
