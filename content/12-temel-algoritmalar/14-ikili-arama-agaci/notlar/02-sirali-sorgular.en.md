What sets a BST apart from a dictionary is order. Two questions a dictionary
cannot answer:

## A range query: the values between 4 and 10

A pruned inorder walk: subtrees that fall outside the range are never
entered.

```python
def in_range(node, lo, hi, out):
    if node is None:
        return out
    if lo < node.value:                # something on the left may be in range
        in_range(node.left, lo, hi, out)
    if lo <= node.value <= hi:
        out.append(node.value)
    if node.value < hi:                # something on the right may be in range
        in_range(node.right, lo, hi, out)
    return out

print(in_range(root, 4, 10, []))
```

```text
[4, 6, 7, 8, 10]
```

`root` is the first tree of the lesson (`8, 3, 10, 1, 6, 14, 4, 7, 13`). `1`,
`13` and `14` were never visited. The cost is `O(h + k)`: `k` is the
number of values found.

## The floor: the largest value not greater than x

```python
def floor(node, x):
    best = None
    while node:
        if node.value == x:
            return x
        if node.value < x:             # a candidate; a larger one may be on the right
            best = node.value
            node = node.right
        else:
            node = node.left
    return best

print(floor(root, 5), floor(root, 12), floor(root, 0))
```

```text
4 10 None
```

`None` because there is no value smaller than `0`. Price brackets and "the
last record before this date" are all this question.

## The same jobs with a sorted list

If the values hardly change, a sorted list and `bisect` answer the same
questions:

```python
import bisect

items = [1, 3, 4, 6, 7, 8, 10, 13, 14]
bisect.insort(items, 5)                     # add without breaking the order
print(items, bisect.bisect_left(items, 7))  # the position of 7
```

```text
[1, 3, 4, 5, 6, 7, 8, 10, 13, 14] 5
```

The slice between `bisect_left(items, lo)` and `bisect_right(items, hi)` is the
answer to the range query.
