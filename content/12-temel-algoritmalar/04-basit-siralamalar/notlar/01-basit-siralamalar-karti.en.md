## The three algorithms at a glance

| | Bubble | Selection | Insertion |
|---|---|---|---|
| Idea | Swap neighbours so the largest rises to the end | Put the smallest of the rest at the front | Slide the next one into place in the sorted part |
| Best case | `O(n)` (with the early exit, a sorted list) | `O(n²)` | `O(n)` (a sorted list) |
| Average / worst | `O(n²)` | `O(n²)` | `O(n²)` |
| Extra memory | `O(1)` | `O(1)` | `O(1)` |
| Stable? | yes | no | yes |
| When? | for teaching | if writing is very expensive | small or nearly sorted lists |

All three sort **in place**: the list itself changes, not a copy (in the
lesson we sorted a copy so the original stays intact).

## Loop boundaries

```python
# Bubble: after each pass the last one settles in place
for end in range(n - 1, 0, -1):
    for i in range(end):              # items[i] with items[i + 1]

# Selection: the smallest after start
for start in range(n - 1):
    for i in range(start + 1, n):

# Insertion: 0..i-1 is sorted, place items[i]
for i in range(1, n):
    j = i - 1
    while j >= 0 and items[j] > current:
```

## Keeping it stable

**Do not swap** equal elements: compare with `>`, not `>=`. Writing
`items[j] >= current` in insertion sort moves an equal element in front of
the other and stability is lost.

## Inversions

The number of pairs standing in the wrong order in a list (`i < j` but
`items[i] > items[j]`) is called the **inversion count**. Bubble sort's swap
count and insertion sort's shift count are exactly the inversion count (both
came out as 250 393 in the lesson). 0 for a sorted list, `n(n−1)/2` for a
reversed one.
