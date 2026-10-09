# Efficient Sorts

Simple sorts are `O(n²)`: about 500 billion comparisons for a million
elements. In this section we write two algorithms that do the same job in
`O(n log n)`, about 20 million comparisons: **merge sort** and **quick sort**.
Both use the recursion of the previous section and both rest on the same
idea: **divide and conquer**. Split the problem into two smaller parts, solve
each part (with yourself), combine the results.

## Merge sort: split, sort, merge

The heart of merge sort is a **merge**: turning two **sorted** lists into one
sorted list. Put a finger at the start of each list; take whichever is
smaller into the result and move that finger on. When one list runs out, add
the rest of the other as it is.

```python
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:            # <=: on ties the left one first (stable)
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])                # one ran out, the rest of the other
    result.extend(right[j:])
    return result
```

Every comparison puts one element into the result; if the two lists have `n`
elements in total, merging is `O(n)`.

Merge sort: a one-element list is already sorted (the base case). Otherwise
split it in the middle, sort each half **with itself**, and merge the two
sorted halves.

```python
def merge_sort(items):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    return merge(merge_sort(items[:mid]), merge_sort(items[mid:]))
```

Printing every call with indentation shows the splitting and the merging:

```text
[38, 27, 43, 3, 9, 82, 10]
  [38, 27, 43]
    [38]
    [27, 43]
      [27]
      [43]
    -> [27, 43]
  -> [27, 38, 43]
  [3, 9, 82, 10]
    [3, 9]
      [3]
      [9]
    -> [3, 9]
    [82, 10]
      [82]
      [10]
    -> [10, 82]
  -> [3, 9, 10, 82]
-> [3, 9, 10, 27, 38, 43, 82]
```

First the list was split down to single elements (each line is a call), then
it was merged back up on the `->` lines.

**Why `O(n log n)`?** The list is halved at every level: reaching single
elements takes `log₂ n` levels. At every level all elements are merged once:
`O(n)` per level. In total `n × log n`.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Level 0</span><span>1 list, 8 elements → merging places 8 elements</span></div>
    <div class="anat-row"><span>Level 1</span><span>2 lists × 4 elements → 8 elements again</span></div>
    <div class="anat-row"><span>Level 2</span><span>4 lists × 2 elements → 8 elements again</span></div>
    <div class="anat-row"><span>Level 3</span><span>8 lists × 1 element → the base case, no merging</span></div>
  </div>
  <figcaption>An 8-element list reaches single elements in 3 levels (log₂ 8 = 3); at every level 8 elements are merged in total: 3 × 8 = n log n.</figcaption>
</figure>

The price of merge sort: merging builds new lists, **`O(n)` extra memory**.
The plus: its worst case is `O(n log n)` too, and it is **stable**.

## Quick sort: split around a pivot

Quick sort does the job the other way round: instead of merging, it **splits
first**. Pick an element from the list (the **pivot**); put the smaller ones
on one side and the larger ones on the other. The pivot is now certainly in
its right place: everything on its left is smaller, everything on its right
larger. Then sort the two sides with itself; no merging is needed, placing
them side by side is enough.

```python
def quick_sort(items):
    if len(items) <= 1:
        return items
    pivot = items[-1]                     # pick the last element as pivot
    smaller = [x for x in items[:-1] if x < pivot]
    larger = [x for x in items[:-1] if x >= pivot]
    return quick_sort(smaller) + [pivot] + quick_sort(larger)
```

For clarity this version builds new lists; real implementations do the same
idea **in place** (by swapping elements) (it is in the note).

If the pivot splits the list into two equal halves, it is like merge sort:
`log n` levels with `n` work per level, `O(n log n)`. On random data the
pivot mostly falls "near enough to the middle".

## We counted: is it really n log n?

On random lists we counted the comparisons of the two algorithms and
compared them with `n log₂ n`:

| n | n log₂ n | Merge sort | Quick sort | Simple sort (n²/2) |
|---|---|---|---|---|
| 1 000 | 9 966 | 8 700 | 11 291 | 499 500 |
| 10 000 | 132 877 | 120 404 | 158 746 | 49 995 000 |
| 100 000 | 1 660 964 | 1 536 526 | 2 049 758 | 4 999 950 000 |

Both stay very close to `n log₂ n`; the simple sorts' `n²/2` reaches 5
billion at a hundred thousand. Quick sort makes a few more comparisons, but in
practice its in-place version is very fast because it is memory-friendly.

## Quick sort's bad day

If the pivot always turns out to be the **smallest** or the **largest**
element, one side is empty and the other has `n − 1` elements: the list
shrinks by only one per level. The version that takes the last element as
pivot does exactly this on an **already sorted** list:

```python
def quick_sort_counting(items, count):
    if len(items) <= 1:
        return items
    pivot = items[-1]
    smaller, larger = [], []
    for x in items[:-1]:
        count[0] += 1                    # one comparison with the pivot
        if x < pivot:
            smaller.append(x)
        else:
            larger.append(x)
    left = quick_sort_counting(smaller, count)
    right = quick_sort_counting(larger, count)
    return left + [pivot] + right

count = [0]
quick_sort_counting(list(range(900)), count)
print(900, count[0])

try:
    quick_sort_counting(list(range(5000)), [0])
except RecursionError as error:
    print("RecursionError -", error)
```

```text
900 404550
RecursionError - maximum recursion depth exceeded
```

`n²/2` comparisons on 900 sorted elements (the worst case is `O(n²)`), and on
5000 elements the recursion depth rose to 5000 and Python stopped it. In real
life data often arrives **already sorted** or nearly sorted; that is why the
pivot is not chosen this way. The fixes:

- **A random pivot:** `random.choice(items)`. No input can keep producing bad
  pivots; the expected time is `O(n log n)`.
- **Median of three:** taking the median of the first, middle and last
  elements as the pivot.

## Can we do better?

No algorithm that sorts by comparing can do meaningfully better than
`n log n` in the worst case. The rough intuition: `n` elements have `n!`
different orderings, and each comparison ("is a bigger than b?") at best
halves the possibilities; getting down to the right ordering needs
`log₂(n!)` comparisons, which is about `n log₂ n`. The only way past this
limit is **not to compare**: counting sorts, in the next section.

## Python's sort: Timsort

`sorted` and `list.sort` use **Timsort**: a combination of merge sort and
insertion sort. It finds the pieces of the data that are already in order
(**runs**), fixes small pieces with insertion sort, and merges the runs like
merge sort. Its worst case is `O(n log n)`, it approaches `O(n)` on sorted or
nearly sorted data, and it is **stable**.

We sorted 200 000 random numbers with our own merge sort:

```text
merge_sort (random)  : 519.7 ms
sorted     (random)  : 35.8 ms
sorted     (sorted)  : 2.8 ms
```

`sorted` is many times faster than our merge sort: the algorithm is similar,
but it is written in C and well tuned. On the already sorted list it
recognised the run and did hardly any work. That is why real code **always**
uses `sorted`; writing your own sort is for understanding the idea and for
being able to build similar algorithms (external sorting, merging two sorted
files).

## Summary

- Divide and conquer: split, solve the parts with yourself, combine.
- Merge sort: split in the middle, sort both halves, **merge**; always
  `O(n log n)`, stable, `O(n)` extra memory.
- Quick sort: **split** around a pivot, sort both sides; `O(n log n)` on
  average, `O(n²)` at worst (a bad pivot on sorted data); a random pivot
  prevents it.
- Sorting by comparison cannot beat `n log n`.
- Python's `sorted` is Timsort: merge + insertion, uses runs, stable; always
  the one in real code.
