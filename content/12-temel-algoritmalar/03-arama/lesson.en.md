# Searching

We already know the simplest way to find a value in a list: **linear
search**, looking from start to end, `O(n)`. If the list is unordered there
is nothing better; you cannot say "missing" without looking at every
element. But if the list is **sorted**, everything changes.

## Searching a sorted list: binary search

Looking up "kite" in a dictionary, you do not start from the first page. You
open it in the middle: if you land on "m", the word is **further back**; you
never open the second half again. Then you open the middle of what is left.
Every look discards **half** of the remaining space.

This is called **binary search**. Its pseudocode:

```text
lo ← 0, hi ← last index
while lo ≤ hi:
    mid ← (lo + hi) // 2
    if list[mid] = target: result: mid
    if list[mid] < target: lo ← mid + 1     (target is to the right)
    else: hi ← mid - 1                       (target is to the left)
result: missing (-1)
```

`lo` and `hi` are the two ends of the region we are searching. Every round
we look at the middle element and throw away half the region. In Python,
printing the region every round:

```python
def binary_search(items, target):
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        print(lo, hi, mid, items[mid])
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(data, 23))
print(binary_search(data, 40))
```

```text
0 9 4 16
5 9 7 56
5 6 5 23
5
0 9 4 16
5 9 7 56
5 6 5 23
6 6 6 38
-1
```

We found 23 in three looks (columns: `lo`, `hi`, `mid`, the middle value).
For 40, after four looks the region became empty (`lo > hi`) and `-1` came
back: 40 is not in the list.

<figure class="fig">
  <div class="versus">
    <div><h4>Linear search</h4>
      <p>Looks at every element from start to end.</p>
      <p>The list need not be sorted.</p>
      <p>Worst case on 1 000 000 elements: <b>1 000 000</b> looks, <code>O(n)</code></p></div>
    <div class="ok"><h4>Binary search</h4>
      <p>Throws away half of the remaining region at every look.</p>
      <p>The list must be <b>sorted</b>.</p>
      <p>Worst case on 1 000 000 elements: <b>20</b> looks, <code>O(log n)</code></p></div>
  </div>
  <figcaption>The payoff of being sorted: searching goes from linear to logarithmic.</figcaption>
</figure>

Because the region halves every round, binary search is `O(log n)`: at most
20 looks among a million elements, 30 among a billion. Linear search may
need a billion looks on the same list.

**Precondition:** the list must be sorted. On an unordered list binary
search gives a wrong answer without raising an error, which is what makes
it dangerous.

## The one-character bug

The idea of binary search is simple, its boundaries are not. Writing the
loop condition as `lo < hi` instead of `lo <= hi` looks harmless:

```python
def binary_search_wrong(items, target):
    lo, hi = 0, len(items) - 1
    while lo < hi:                     # should have been <=
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print([binary_search_wrong(data, x) for x in data])
```

```text
[-1, 1, 2, -1, 4, 5, -1, 7, 8, -1]
```

**4 of the 10 values** in the list were not found. When the region shrinks
to a single element (`lo == hi`), the loop ends without looking at it. Such
bugs may not show on an ordinary example; searching for **every** value in
the list catches them.

In binary search three things must agree with each other:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Start</span><span><code>lo = 0</code>, <code>hi = len(items) - 1</code>: both ends are <b>inside</b> the searched region.</span></div>
    <div class="anat-row"><span>Loop condition</span><span><code>lo &lt;= hi</code>: a one-element region is looked at too.</span></div>
    <div class="anat-row"><span>Narrowing</span><span><code>lo = mid + 1</code> or <code>hi = mid - 1</code>: the <code>mid</code> just checked leaves the region, so it shrinks every round.</span></div>
  </div>
  <figcaption>Together the three describe a range with both ends included. Change one and you have to make the others agree with it.</figcaption>
</figure>

Writing `lo = mid` instead of `mid + 1` can do worse: the region never
shrinks and the loop runs **forever**.

## Finding the first occurrence

If the list contains repeated values, binary search finds **some**
occurrence of the value. Often we want the **first**: "the first student with
a score of 55". For that we do not stop at a match; we note the answer and
**keep searching to the left**:

```python
def first_occurrence(items, target):
    lo, hi = 0, len(items) - 1
    answer = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            answer = mid          # found it, but there may be one further left
            hi = mid - 1
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return answer
```

Still `O(log n)`: the region still halves every round.

## The ready-made one: the `bisect` module

Python's standard library has a ready-made, bug-free binary search. The
`bisect` module finds **where a value belongs** in a sorted list:

- `bisect_left(items, x)`: the **leftmost** place `x` could go (so the first
  occurrence, if `x` is there).
- `bisect_right(items, x)`: the **rightmost** place `x` could go (one past
  the last occurrence).
- `insort(items, x)`: inserts `x` without breaking the order.

```python
import bisect

scores = [40, 55, 55, 55, 70, 85, 90]
print(bisect.bisect_left(scores, 55), bisect.bisect_right(scores, 55))
print(bisect.bisect_right(scores, 55) - bisect.bisect_left(scores, 55))
print(bisect.bisect_left(scores, 60))
bisect.insort(scores, 60)
print(scores)
```

```text
1 4
3
4
[40, 55, 55, 55, 60, 70, 85, 90]
```

The difference between the two boundaries gives **how many times** the value
occurs, in `O(log n)`: 55 is there three times. 60 is not in the list, but we
know its place is index 4. Careful: `insort` finds the place in `O(log n)`,
but inserting shifts the ones behind it, so it is `O(n)`.

## Binary search on the answer

Binary search works not only on lists but on any question **whose yes/no
answer flips at some point**. Example: the integer square root of `n`, the
largest `k` with `k * k <= n`. As `k` grows, `k * k <= n` is true at first
and then false for good. We find that boundary with binary search, halving
the range between `0` and `n` every round. You will write this in the
exercises. The same idea works for questions like "how few servers are
enough?" or "how many people fit at most?".

## When is sorting worth it?

For a single search in an unordered list, linear search (`O(n)`) is best:
sorting alone is `O(n log n)`. But if you will do **many** searches on the
same list, sorting once and then doing each search in `O(log n)` wins. If
only "is it there?" is asked, a set is even better; but a set cannot answer
"the first value above 60" or "how many values between 40 and 70?", and a
sorted list can.

## Summary

- Searching an unordered list is `O(n)`; binary search on a sorted list is
  `O(log n)`.
- Binary search throws away half the region every round; its precondition
  is a sorted list.
- The boundaries must agree: `lo <= hi`, `lo = mid + 1`, `hi = mid - 1`.
  Bugs only show when every value and the edge cases are tried.
- For the first occurrence, do not stop at a match; keep searching left.
- The ready-made version is `bisect`: `bisect_left`, `bisect_right`,
  `insort`.
- Binary search works for any question "whose answer flips at some point".
