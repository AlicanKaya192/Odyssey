# Two Pointers and Sliding Window

When looking for "a pair meeting some condition" or "a consecutive piece
meeting some condition" in a list, the first solution that comes to mind is
to try every pair, every piece: `O(n²)`. The two techniques in this section
solve the same questions **by going through the list once**: **two pointers**
and the **sliding window**. The idea in both is the same: do not throw away
what the previous step taught you.

## Two pointers: inwards from both ends

**Problem:** in a sorted list of prices, are there two prices that add up to
exactly `target`?

Brute force tries every pair. Two pointers put one pointer at the start
(`left`) and one at the end (`right`) and look at the sum:

- If the sum is **too small**: a bigger number is needed; move `left` one
  step right.
- If the sum is **too big**: a smaller number is needed; move `right` one
  step left.
- If it is **equal**: found it.

```python
def pair_two_pointers(items, target):
    left, right = 0, len(items) - 1
    while left < right:
        total = items[left] + items[right]
        if total == target:
            return items[left], items[right]
        if total < target:
            left += 1          # a bigger number is needed
        else:
            right -= 1         # a smaller number is needed
    return None
```

**Why is it correct?** When the sum is too small, skipping `left` is safe:
`items[left]` cannot reach the target even with the largest number
(`items[right]`), so it is useless in any pair. The same logic applies to
`right` when it is too big. Every step certainly rules out one candidate, and
the pointers meet in at most `n` steps: `O(n)`.

We added a step counter to both functions and compared them with brute force
(10 000 sorted prices):

```text
((0, 19990), 9995)
((0, 19990), 5)
(None, 49995000)
(None, 9999)
```

Columns: the pair found and the number of steps. The first two lines are the
case where the answer sits at the two ends of the list; the last two are
**when there is no answer**: brute force must try every pair (almost 50
million), two pointers say "none" in 9 999 steps.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>[1, 3, 4, 6, 9]</code>, target 10</span><span>left → 1, right → 9: sum 10, found</span></div>
    <div class="anat-row"><span><code>[1, 3, 4, 6, 9]</code>, target 7</span><span>1 + 9 = 10 too big → right moves left (6)</span></div>
    <div class="anat-row"><span></span><span>1 + 6 = 7, found</span></div>
    <div class="anat-row"><span><code>[1, 3, 4, 6, 9]</code>, target 14</span><span>1 + 9 = 10 too small → left moves right; 3 + 9 = 12 too small → left right; 4 + 9 = 13 too small → left right; 6 + 9 = 15 too big → right moves left; the pointers met: none</span></div>
  </div>
  <figcaption>Every step certainly rules out one candidate; the pointers never go back.</figcaption>
</figure>

Precondition: the list is **sorted**. For an unsorted list the same question
uses the set lookup method from earlier sections (details in the Hashing
section).

## Two pointers in the same direction: fast and slow

The pointers can also walk in the same direction. Removing repeats from a
sorted list **in place**:

```python
def remove_duplicates(items):
    if not items:
        return 0
    slow = 0                              # where the last unique value was written
    for fast in range(1, len(items)):     # the reading pointer
        if items[fast] != items[slow]:
            slow += 1
            items[slow] = items[fast]
    return slow + 1                       # the number of unique elements
```

`fast` reads every element, `slow` writes only when it sees a new value. No
extra list: `O(n)` time, `O(1)` extra memory.

## Sliding window: fixed size

**Problem:** in daily sales, during which period is the total of `k`
consecutive days the largest?

Brute force adds `k` numbers from scratch for every starting day:
`O(n × k)`. But when a window slides by one day, only two parts of the sum
change: **the day coming in is added, the day going out is subtracted**.

```python
def best_window(values, k):
    total = sum(values[:k])               # the first window
    best = total
    for i in range(k, len(values)):
        total += values[i] - values[i - k]   # in - out
        if total > best:
            best = total
    return best
```

We measured the steps (counting every addition) taken by the two methods for
a 500-day window over 10 000 days:

```text
(26476, 4750500)
(26476, 10000)
```

The same answer (the first number), about 475 times less work.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Values</span><span><code>[4, 2, 7, 1, 8, 3]</code>, k = 3</span></div>
    <div class="anat-row"><span>Window 1: 4, 2, 7</span><span>sum 13</span></div>
    <div class="anat-row"><span>Window 2: 2, 7, 1</span><span>13 + 1 − 4 = 10</span></div>
    <div class="anat-row"><span>Window 3: 7, 1, 8</span><span>10 + 8 − 2 = 16</span></div>
    <div class="anat-row"><span>Window 4: 1, 8, 3</span><span>16 + 3 − 7 = 12</span></div>
  </div>
  <figcaption>Only two operations per slide: the one coming in is added, the one going out subtracted. The largest sum is 16.</figcaption>
</figure>

## Sliding window: variable size

Sometimes the window has no fixed size; it grows while a **condition** holds
and shrinks from the left when it breaks. Example: the **longest piece of a
string with no repeated letter**.

```python
def longest_unique(text):
    last_seen = {}                 # letter → the index where it was last seen
    start = 0                      # the window's left end
    best = 0
    for end, ch in enumerate(text):
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1     # a repeat: move the left end past it
        last_seen[ch] = end
        best = max(best, end - start + 1)
    return best

for t in ["abcabcbb", "bbbbb", "pwwkew", ""]:
    print(repr(t), longest_unique(t))
```

```text
'abcabcbb' 3
'bbbbb' 1
'pwwkew' 3
'' 0
```

The right end (`end`) moves on one step every round, the left end (`start`)
only ever moves forward; together they take at most `n` steps: `O(n)`.
Trying every possible piece would be `O(n²)` (even `O(n³)` with checking
whether the piece has no repeats).

## Which one for which problem?

- **Finding a pair/triple in a sorted list** (with this sum, with that
  difference): pointers from both ends.
- **Rearranging in place** (drop repeats, move zeros to the end): fast and
  slow pointers.
- **A consecutive piece** (the largest sum, an average, the shortest/longest
  piece meeting a condition): a sliding window.

A shared hint: if the problem says "consecutive" or "sorted" and the brute
force is a nested loop, a solution where the pointers only ever move
**forward** very likely exists.

## Summary

- Two pointers: inwards from both ends of a sorted list; each step rules out
  one candidate, `O(n)`.
- Fast/slow pointers: in the same direction, rearranging in place, `O(1)`
  extra memory.
- Fixed window: when sliding, add the one coming in and subtract the one
  going out; `O(n)` instead of `O(n × k)`.
- Variable window: the left end moves on when the condition breaks; both ends
  take `O(n)` steps in total.
- As long as the pointers never go back, the total work stays linear.
