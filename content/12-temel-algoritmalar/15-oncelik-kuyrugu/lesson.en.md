# Priority Queues and Heaps

In a hospital's emergency room patients are seen not in order of arrival but
by **urgency**. The same need comes up often in computing: the operating
system runs the important task first, a map app looking for the shortest
route always opens the "closest so far" point, a model keeps its best `k`
predictions. This is called a **priority queue**: add elements in any order,
take **the smallest** (the highest priority) every time.

Both simple ways get stuck somewhere:

| Structure | Add | Take the smallest |
|---|---|---|
| Unsorted list | `O(1)` | `O(n)` (look at all) |
| Sorted list | `O(n)` (shifting) | `O(1)` |
| **Heap** | `O(log n)` | `O(log n)` |

## What is a heap?

A **heap** is a binary tree with two rules:

1. **Shape:** the tree fills level by level, left to right, **without gaps**
   (a complete binary tree). So its height is always `≈ log₂ n`; the BST's
   chain problem never comes up.
2. **Order:** every node is **smaller than or equal to its children**
   (a min-heap). So the smallest value is always **at the root**.

The difference from a BST: there is no order between siblings. A heap is not
fully sorted, only sorted "enough to find the smallest at once". And that
much is cheap.

## A tree embedded in an array

Because the shape rule leaves no gaps, a heap can be kept not with node
objects but in **a plain list**. The levels are written left to right in
order:

<figure class="fig">
<svg viewBox="0 0 350 180" width="350" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="79.0" y1="89.0" x2="23.0" y2="153.0"/>
<line class="line" x1="79.0" y1="89.0" x2="135.0" y2="153.0"/>
<line class="line" x1="303.0" y1="89.0" x2="247.0" y2="153.0"/>
<line class="line" x1="191.0" y1="25.0" x2="79.0" y2="89.0"/>
<line class="line" x1="191.0" y1="25.0" x2="303.0" y2="89.0"/>
<circle class="box" cx="23.0" cy="153.0" r="17"/>
<circle class="curve4" cx="23.0" cy="153.0" r="17"/>
<text class="ink" x="23.0" y="157.9" font-size="14" text-anchor="middle">5</text>
<circle class="box" cx="79.0" cy="89.0" r="17"/>
<circle class="curve" cx="79.0" cy="89.0" r="17"/>
<text class="ink" x="79.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="135.0" cy="153.0" r="17"/>
<circle class="curve4" cx="135.0" cy="153.0" r="17"/>
<text class="ink" x="135.0" y="157.9" font-size="14" text-anchor="middle">9</text>
<circle class="box" cx="191.0" cy="25.0" r="17"/>
<text class="ink" x="191.0" y="29.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="247.0" cy="153.0" r="17"/>
<text class="ink" x="247.0" y="157.9" font-size="14" text-anchor="middle">8</text>
<circle class="box" cx="303.0" cy="89.0" r="17"/>
<text class="ink" x="303.0" y="93.9" font-size="14" text-anchor="middle">2</text>
</svg>
<svg viewBox="0 0 350 66" width="350" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="18" font-size="12">index</text>
<text class="dim" x="93.0" y="18" font-size="12" text-anchor="middle">0</text>
<rect class="box" x="70" y="26" width="46" height="36"/>
<text class="ink" x="93.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="139.0" y="18" font-size="12" text-anchor="middle">1</text>
<rect class="box" x="116" y="26" width="46" height="36"/>
<rect class="curve" x="118" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="139.0" y="48.9" font-size="14" text-anchor="middle">3</text>
<text class="dim" x="185.0" y="18" font-size="12" text-anchor="middle">2</text>
<rect class="box" x="162" y="26" width="46" height="36"/>
<text class="ink" x="185.0" y="48.9" font-size="14" text-anchor="middle">2</text>
<text class="dim" x="231.0" y="18" font-size="12" text-anchor="middle">3</text>
<rect class="box" x="208" y="26" width="46" height="36"/>
<rect class="curve4" x="210" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="231.0" y="48.9" font-size="14" text-anchor="middle">5</text>
<text class="dim" x="277.0" y="18" font-size="12" text-anchor="middle">4</text>
<rect class="box" x="254" y="26" width="46" height="36"/>
<rect class="curve4" x="256" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="277.0" y="48.9" font-size="14" text-anchor="middle">9</text>
<text class="dim" x="323.0" y="18" font-size="12" text-anchor="middle">5</text>
<rect class="box" x="300" y="26" width="46" height="36"/>
<text class="ink" x="323.0" y="48.9" font-size="14" text-anchor="middle">8</text>
</svg>
<figcaption>The same heap as a tree and as a list. The children of 3 at index 1 (purple) are at indexes 2·1 + 1 = 3 and 2·1 + 2 = 4: 5 and 9 (green).</figcaption>
</figure>

The children of the node at index `i` are `2i + 1` and `2i + 2`, its parent
is `(i - 1) // 2`. No pointers, no extra memory. Python's `heapq` module does
exactly this.

## With `heapq`

```python
import heapq

heap = []
for x in [5, 3, 8, 1, 9, 2]:
    heapq.heappush(heap, x)
print(heap)
print(heapq.heappop(heap), heapq.heappop(heap), heap)
```

```text
[1, 3, 2, 5, 9, 8]
1 2 [3, 5, 8, 9]
```

The list is **not sorted** (`[1, 3, 2, ...]`), but `heap[0]` is always the
smallest and `heappop` gives the next smallest every time.

## What happens inside?

**Adding (sift up):** the new value is put at the end of the list, that is in
the lowest empty spot of the tree. As long as it is smaller than its parent,
it swaps places with it and moves up:

```python
def push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] >= heap[parent]:     # the rule holds
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent

h = []
for x in [5, 3, 8, 1, 9, 2]:
    push(h, x)
print(h)
```

```text
[1, 3, 2, 5, 9, 8]
```

The same list as with `heapq`. At most as many steps as the tree's height:
`O(log n)`.

**Taking the smallest (sift down):** the root is taken and the **last**
element of the list is put in its place. If this element is large, the rule
breaks; it moves down by swapping with its **smaller child**, and stops when
it is smaller than both children. Again `O(log n)`. You will write this
yourself in the exercise.

## heapify and heap sort

If you already have a list, there is no need to add the elements one by one:
`heapq.heapify` turns the list into a heap **in place**, and does it in
`O(n)`. Then `n` calls of `heappop` give the values sorted: **heap sort**,
`O(n log n)`.

```python
data = [5, 3, 8, 1, 9, 2]
heapq.heapify(data)
print(data)
print([heapq.heappop(data) for _ in range(len(data))])
```

```text
[1, 3, 2, 5, 9, 8]
[1, 2, 3, 5, 8, 9]
```

For sorting in Python `sorted` is faster (it is written in C and uses the
sorted runs inside the data). Heap sort's value is that it can be done in
place without extra memory and stays `O(n log n)` even in the worst case.

## The k largest elements

To get the 10 largest of a million numbers, sorting the whole list is
wasteful. `heapq.nlargest` keeps a heap of size `k`:

```text
same result      : True
sorted(...)[:10] : 141.7 ms
heapq.nlargest   : 10.7 ms
```

The same result, many times faster. The idea: to find the largest
`k`, keep a **min-heap** of size `k`. The root holds **the smallest** of the
largest `k` so far; if a new number is larger than it, drop the root and put
the new number in:

```python
def top_k(stream, k):
    heap = []
    for x in stream:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:                  # larger than the root: make room
            heapq.heapreplace(heap, x)     # pop + push in one step
    return sorted(heap, reverse=True)

print(top_k([4, 1, 7, 3, 9, 2, 8], 3))
```

```text
[9, 8, 7]
```

The cost is `O(n log k)` and the memory only `O(k)`: it works even if the
data comes line by line from a file or a stream.

## Prioritised tasks: tuples

When you put `(priority, value)` tuples in a heap, the tuples are compared by
their first element:

```python
tasks = []
heapq.heappush(tasks, (2, "write report"))
heapq.heappush(tasks, (1, "fix bug"))
heapq.heappush(tasks, (3, "lunch"))
while tasks:
    print(heapq.heappop(tasks))
```

```text
(1, 'fix bug')
(2, 'write report')
(3, 'lunch')
```

A trap: if two tasks have **equal** priority, Python compares the second
elements. If those cannot be compared (like dictionaries), you get an error:

```python
jobs = []
heapq.heappush(jobs, (1, {"name": "a"}))
heapq.heappush(jobs, (1, {"name": "b"}))
```

```text
TypeError: '<' not supported between instances of 'dict' and 'dict'
```

The fix is to put an increasing counter in between: `(priority, number,
value)`. On a tie the counter decides, and equal priorities come out **in
order of arrival**. `itertools.count()` gives this counter.

## Max-heap

`heapq` is a min-heap. There are two ways to take the largest: put the values
in **negated** (`heappush(h, -x)`, and negate again when taking) or use the
max-heap functions that came with Python 3.14:

```python
m = [5, 3, 8, 1, 9, 2]
heapq.heapify_max(m)
print(m, heapq.heappop_max(m))
```

```text
[8, 5, 2, 1, 3] 9
```

## Merging sorted lists

To merge `k` sorted lists into one sorted list, put the **first** element of
each list in a heap, take the smallest, and add the next one from that list.
`heapq.merge` does this lazily, producing elements as you ask for them:

```python
print(list(heapq.merge([1, 4, 9], [2, 3, 10], [5])))
```

```text
[1, 2, 3, 4, 5, 9, 10]
```

This is the classic way to sort a file that does not fit in memory: sort it
piece by piece, write the pieces to disk, then merge them with `merge`
(external sort). The same piece-by-piece idea as in the Big Data path.

## In data science

- **k-nearest neighbours:** the `k` examples closest to a point, the same as
  `top_k` over the distances (the smallest `k`).
- **Recommender systems:** the best 20 of the scores of millions of products;
  a heap, not a sort.
- **Shortest paths:** Dijkstra's algorithm in the Algorithm Techniques module takes "the closest
  unopened node" from a priority queue.

## Summary

- A priority queue: add in any order, always take the smallest. A heap does
  both in `O(log n)`; looking at the smallest is `O(1)`.
- A heap: a gap-free binary tree + parent ≤ child. In a plain list: children
  `2i+1`, `2i+2`, parent `(i-1)//2`.
- Adding sifts up, taking sifts down. `heapify` is `O(n)`, heap sort
  `O(n log n)`.
- The largest `k`: a min-heap of size `k`, `O(n log k)`; `heapq.nlargest`.
- A counter for ties in tuples: `(priority, number, value)`.
- Max-heap: negate, or `heapify_max` / `heappop_max`.
- `heapq.merge`: merges sorted lists lazily.
