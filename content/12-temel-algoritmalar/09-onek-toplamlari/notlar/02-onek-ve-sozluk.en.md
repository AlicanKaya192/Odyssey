Three common variants of the "prefix sum + dictionary" pattern. In all
three the list is walked once: `O(n)`.

## 1. The longest piece adding up to k

Store not the count but **the index where a prefix sum was first seen**: the
longest piece needs the leftmost start.

```python
def longest_sum_k(values, k):
    first_index = {0: -1}          # the empty prefix, at position -1
    total = 0
    best = 0
    for i, x in enumerate(values):
        total += x
        if total - k in first_index:
            best = max(best, i - first_index[total - k])
        if total not in first_index:   # keep only the first sighting
            first_index[total] = i
    return best

print(longest_sum_k([1, -1, 5, -2, 3], 3))   # 4  (1, -1, 5, -2)
```

## 2. The longest piece with as many 0s as 1s

Count every `0` as `-1`; "as many" then means "sums to 0". So the question
becomes variant 1 (`k = 0`).

```python
def longest_balanced(bits):
    return longest_sum_k([1 if b == 1 else -1 for b in bits], 0)

print(longest_balanced([0, 1, 0, 0, 1, 1, 0]))   # 6
```

## 3. Counting the pieces whose sum divides by k

If the difference of two prefix sums divides by `k`, their remainders modulo
`k` are equal. Count remainders in the dictionary:

```python
def count_divisible(values, k):
    seen = {0: 1}
    total = 0
    count = 0
    for x in values:
        total += x
        r = total % k                  # 0..k-1 in Python even for negatives
        count += seen.get(r, 0)
        seen[r] = seen.get(r, 0) + 1
    return count

print(count_divisible([4, 5, 0, -2, -3, 1], 5))   # 7
```

## When to use this pattern?

If the question involves **"a consecutive piece"** and **"a sum/mean/
balance"** and the numbers can be negative, try this pattern first. If the
numbers are always positive, a sliding window is enough and needs no
dictionary.
