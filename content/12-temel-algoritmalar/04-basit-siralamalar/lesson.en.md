# Simple Sorts

Sorting is the most studied topic in algorithms: as we saw in the previous
section, searching a sorted list drops to `O(log n)`; finding repeats, taking
the median and comparing two lists all get easier. In Python sorting is one
line (`sorted(items)`), but without knowing the ideas inside it we cannot
understand why it is fast or slow on which data.

In this section we write three **simple** sorts ourselves. All three are
`O(n²)`; slow on large lists. But they carry very important ideas, and one
of them (insertion sort) still runs inside Python's own sort today.

In the examples the functions sort and return a **copy** of the list
(`items[:]`); the original list does not change.

## Bubble sort

The idea: compare two neighbours and swap them if they are in the wrong
order. After one **pass** like this from the start of the list to the end,
the largest element has moved to the end, like a bubble rising to the
surface. Then repeat the same for the rest.

```python
def bubble_sort(items):
    items = items[:]
    n = len(items)
    passes = 0
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        passes += 1
        print(passes, items)
        if not swapped:          # no swap in this pass means the list is sorted
            break
    return items

bubble_sort([5, 1, 4, 2, 8])
```

```text
1 [1, 4, 2, 5, 8]
2 [1, 2, 4, 5, 8]
3 [1, 2, 4, 5, 8]
```

In the first pass 8 was already at the end and 5 moved towards it. After the
second pass the list was sorted; the third pass made no swap, and thanks to
`swapped` the loop ended early. Without that small check the algorithm would
do every pass even on a sorted list.

`a, b = b, a` is Python's short way of swapping two variables: the tuple on
the right is built first, then unpacked to the left.

## Selection sort

The idea: **find the smallest** among the rest of the list and put it at the
front. Then do the same from the second place on. It is like running the
"where is the smallest" function from earlier sections again and again.

```python
def selection_sort(items):
    items = items[:]
    for start in range(len(items) - 1):
        smallest = start
        for i in range(start + 1, len(items)):
            if items[i] < items[smallest]:
                smallest = i
        items[start], items[smallest] = items[smallest], items[start]
        print(start, items)
    return items

selection_sort([29, 10, 14, 37, 13])
```

```text
0 [10, 29, 14, 37, 13]
1 [10, 13, 14, 37, 29]
2 [10, 13, 14, 37, 29]
3 [10, 13, 14, 29, 37]
```

Each round makes a single swap; that is why selection sort used to be
preferred where writing was expensive (memories where swapping is costly).
But its comparison count is **always** the same: even if the list is already
sorted, it looks at every remaining element to find the smallest.

## Insertion sort

The idea: what you do when sorting playing cards in your hand. The left part
is always sorted; you take the next card and **slide it left to its right
place** in the sorted part.

```python
def insertion_sort(items):
    items = items[:]
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]      # shift the bigger one right
            j -= 1
        items[j + 1] = current           # place it in the gap
        print(i, items)
    return items

insertion_sort([12, 11, 13, 5, 6])
```

```text
1 [11, 12, 13, 5, 6]
2 [11, 12, 13, 5, 6]
3 [5, 11, 12, 13, 6]
4 [5, 6, 11, 12, 13]
```

In the second round 13 was already in place; the `while` loop did not run at
all. That is the strength of insertion sort: on a **nearly sorted** list each
element slides left only a few steps.

## Comparing the three

We sorted the same 1000-element lists with the three algorithms and counted
the comparisons and swaps (shifts for insertion):

| List (n = 1000) | Bubble comp. / swaps | Selection comp. / swaps | Insertion comp. / shifts |
|---|---|---|---|
| Random | 498 015 / 250 393 | 499 500 / 991 | 251 387 / 250 393 |
| Sorted | 999 / 0 | 499 500 / 0 | 999 / 0 |
| Nearly sorted (last 10 shuffled) | 3 990 / 13 | 499 500 / 7 | 1 012 / 13 |
| Reversed | 499 500 / 499 500 | 499 500 / 500 | 499 500 / 499 500 |

What the table shows:

- **On a random list** all three make about `n²/4`–`n²/2` comparisons:
  `O(n²)`.
- **Selection sort** ignores the input entirely: 499 500 comparisons even on
  a sorted list. But it makes the fewest swaps.
- **Insertion sort** makes only `n − 1` comparisons on a sorted list; its
  best case is `O(n)`. On a nearly sorted list it is almost the same.
- **Bubble sort** is fast on a sorted list thanks to the early exit; on a
  random list its comparisons match selection's and its swaps match
  insertion's shifts: it carries the bad side of both. It is rarely chosen
  in practice; it is good for teaching.

In practice only **insertion sort** is used among the simple sorts: it is
very fast on small lists (a few dozen elements) and nearly sorted data.
Python's sort (Timsort) already sorts small pieces with insertion sort.

## Stability

If two elements are **equal** by the sort key (the same score, say) and keep
**their previous order** after sorting, the algorithm is **stable**. Why does
it matter? If you sort a list of students first by name and then by score, a
stable sort does not disturb the name order of those with the same score.

Selection sort is not stable: a long-distance swap can jump over two equal
elements.

```python
def selection_sort_by_score(records):
    records = records[:]
    for start in range(len(records) - 1):
        smallest = start
        for i in range(start + 1, len(records)):
            if records[i][1] < records[smallest][1]:
                smallest = i
        records[start], records[smallest] = records[smallest], records[start]
    return records

students = [("Bora", 2), ("Ada", 2), ("Cem", 1)]
print(selection_sort_by_score(students))
print(sorted(students, key=lambda r: r[1]))
```

```text
[('Cem', 1), ('Ada', 2), ('Bora', 2)]
[('Cem', 1), ('Bora', 2), ('Ada', 2)]
```

Bora, with a score of 2, was ahead of Ada in the input; selection sort
reversed them (swapping Cem and Bora threw Bora behind Ada). Python's
`sorted` is **stable**: Bora stayed ahead. Bubble and insertion sort are
stable too, because they only swap neighbours that are **strictly greater**
(we wrote `>`, not `>=`).

## Sorting in Python: `key=`

Writing our own sort is instructive, but real code uses `sorted` and
`list.sort`. Both take `key=`: a function that extracts a **key** from each
element. Comparisons are made on these keys.

```python
words = ["banana", "Kiwi", "apple", "fig", "pear"]
print(sorted(words))
print(sorted(words, key=str.lower))
print(sorted(words, key=len))
print(sorted(words, key=lambda w: (len(w), w.lower())))
```

```text
['Kiwi', 'apple', 'banana', 'fig', 'pear']
['apple', 'banana', 'fig', 'Kiwi', 'pear']
['fig', 'Kiwi', 'pear', 'apple', 'banana']
['fig', 'Kiwi', 'pear', 'apple', 'banana']
```

- Capital letters come before lowercase ones (`"Kiwi"` first), because
  strings are compared by character codes. `key=str.lower` fixes that.
- `key=len` sorts by length; `"Kiwi"` and `"pear"`, of equal length, stay in
  their input order thanks to stability.
- When the key is a **tuple**, the first item is compared first, then the
  second if equal: "length first, then alphabetical".

`reverse=True` sorts from largest to smallest and still keeps stability.

## Summary

- Bubble: moves the largest to the end by swapping neighbours; fast on a
  sorted list with the early exit.
- Selection: puts the smallest of the rest at the front; always `n²/2`
  comparisons, the fewest swaps; not stable.
- Insertion: slides the next element into place in the sorted part; best
  case `O(n)`, the best on nearly sorted data; stable.
- All three are `O(n²)` in the worst and average case.
- A stable sort keeps the order of elements with equal keys; Python's
  `sorted` is stable.
- In real code, `sorted(items, key=...)`; a tuple key sorts by several
  criteria.
