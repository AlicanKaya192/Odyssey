# Binary Search Trees

Binary search on a sorted list took `O(log n)`, but inserting an element in
the middle is `O(n)` because of the shifting. A dictionary inserts and
searches in `O(1)`, but it does not know **order**: it cannot answer "the
smallest value greater than 6" or "the values between 4 and 10". A **binary
search tree (BST)** sits between the two: as long as the tree stays
balanced, searching, inserting and deleting are `O(log n)`, and the order is
kept.

## One rule

For every node: **all values in the left subtree are smaller than the node,
all values in the right subtree are larger.** The rule holds not only for the
children but for **the whole subtree**.

<figure class="fig">
<svg viewBox="0 0 518 244" width="518" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="191.0" y1="153.0" x2="135.0" y2="217.0"/>
<line class="line" x1="191.0" y1="153.0" x2="247.0" y2="217.0"/>
<line class="line" x1="79.0" y1="89.0" x2="23.0" y2="153.0"/>
<line class="line" x1="79.0" y1="89.0" x2="191.0" y2="153.0"/>
<line class="line" x1="471.0" y1="153.0" x2="415.0" y2="217.0"/>
<line class="line" x1="359.0" y1="89.0" x2="471.0" y2="153.0"/>
<line class="line" x1="303.0" y1="25.0" x2="79.0" y2="89.0"/>
<line class="line" x1="303.0" y1="25.0" x2="359.0" y2="89.0"/>
<circle class="box" cx="23.0" cy="153.0" r="17"/>
<text class="ink" x="23.0" y="157.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="79.0" cy="89.0" r="17"/>
<circle class="curve" cx="79.0" cy="89.0" r="17"/>
<text class="ink" x="79.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="135.0" cy="217.0" r="17"/>
<text class="ink" x="135.0" y="221.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="191.0" cy="153.0" r="17"/>
<circle class="curve" cx="191.0" cy="153.0" r="17"/>
<text class="ink" x="191.0" y="157.9" font-size="14" text-anchor="middle">6</text>
<circle class="box" cx="247.0" cy="217.0" r="17"/>
<text class="ink" x="247.0" y="221.9" font-size="14" text-anchor="middle">7</text>
<circle class="box" cx="303.0" cy="25.0" r="17"/>
<circle class="curve" cx="303.0" cy="25.0" r="17"/>
<text class="ink" x="303.0" y="29.9" font-size="14" text-anchor="middle">8</text>
<circle class="box" cx="359.0" cy="89.0" r="17"/>
<text class="ink" x="359.0" y="93.9" font-size="14" text-anchor="middle">10</text>
<circle class="box" cx="415.0" cy="217.0" r="17"/>
<text class="ink" x="415.0" y="221.9" font-size="14" text-anchor="middle">13</text>
<circle class="box" cx="471.0" cy="153.0" r="17"/>
<text class="ink" x="471.0" y="157.9" font-size="14" text-anchor="middle">14</text>
</svg>
<figcaption>The tree built by inserting 8, 3, 10, 1, 6, 14, 4, 7, 13 in order. The purple rings are the search path for 6: 6 &lt; 8 left, 6 &gt; 3 right.</figcaption>
</figure>

The gift of this rule shows up in the **inorder** walk from the Trees section:
the order left, root, right gives the values **from smallest to largest**.

## Inserting

A new value starts at the root and goes down left or right by the rule until
it is put in an empty spot. The same recursive skeleton as in the Trees
section:

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def insert(node, value):
    if node is None:                       # an empty spot was found
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node                            # if equal, do not add: no repeats

def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)

root = None
for v in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    root = insert(root, v)
print(inorder(root))
```

```text
[1, 3, 4, 6, 7, 8, 10, 13, 14]
```

The values arrived in mixed order, inorder gave them sorted. This tree is the
one in the figure above.

## Searching

At each step a whole subtree is ruled out, just like half of the list in
binary search:

```python
def search(node, target):
    path = []
    while node:
        path.append(node.value)
        if target == node.value:
            return True, path
        node = node.left if target < node.value else node.right
    return False, path

print(search(root, 6))
print(search(root, 5))
```

```text
(True, [8, 3, 6])
(False, [8, 3, 6, 4])
```

`6` was found in three steps (the path with purple rings in the figure). Even
though `5` is missing, the search was short: the right of `4` is empty, and
`5` would be there if it existed. The number of steps is at most the tree's
**height**: `O(h)`.

The smallest value is in the leftmost node, the largest in the rightmost:

```python
def minimum(node):
    while node.left:
        node = node.left
    return node.value
```

## Deleting: three cases

Deleting is the hardest operation, because the rule must not break when the
node goes:

1. **A leaf:** removed directly.
2. **One child:** the child takes the deleted node's place.
3. **Two children:** the node is replaced by **the next value (the inorder
   successor)**: the smallest in the right subtree. That value is larger
   than the node but smaller than everything else in the right subtree, so
   the rule holds. Then that value is deleted from the right subtree (there
   it has at most one child).

<figure class="fig">
<svg viewBox="0 0 518 244" width="518" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="191.0" y1="153.0" x2="135.0" y2="217.0"/>
<line class="line" x1="191.0" y1="153.0" x2="247.0" y2="217.0"/>
<line class="line" x1="79.0" y1="89.0" x2="23.0" y2="153.0"/>
<line class="line" x1="79.0" y1="89.0" x2="191.0" y2="153.0"/>
<line class="line" x1="471.0" y1="153.0" x2="415.0" y2="217.0"/>
<line class="line" x1="359.0" y1="89.0" x2="471.0" y2="153.0"/>
<line class="line" x1="303.0" y1="25.0" x2="79.0" y2="89.0"/>
<line class="line" x1="303.0" y1="25.0" x2="359.0" y2="89.0"/>
<circle class="box" cx="23.0" cy="153.0" r="17"/>
<text class="ink" x="23.0" y="157.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="79.0" cy="89.0" r="17"/>
<circle class="curve2" cx="79.0" cy="89.0" r="17"/>
<text class="ink" x="79.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="135.0" cy="217.0" r="17"/>
<circle class="curve4" cx="135.0" cy="217.0" r="17"/>
<text class="ink" x="135.0" y="221.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="191.0" cy="153.0" r="17"/>
<text class="ink" x="191.0" y="157.9" font-size="14" text-anchor="middle">6</text>
<circle class="box" cx="247.0" cy="217.0" r="17"/>
<text class="ink" x="247.0" y="221.9" font-size="14" text-anchor="middle">7</text>
<circle class="box" cx="303.0" cy="25.0" r="17"/>
<text class="ink" x="303.0" y="29.9" font-size="14" text-anchor="middle">8</text>
<circle class="box" cx="359.0" cy="89.0" r="17"/>
<text class="ink" x="359.0" y="93.9" font-size="14" text-anchor="middle">10</text>
<circle class="box" cx="415.0" cy="217.0" r="17"/>
<text class="ink" x="415.0" y="221.9" font-size="14" text-anchor="middle">13</text>
<circle class="box" cx="471.0" cy="153.0" r="17"/>
<text class="ink" x="471.0" y="157.9" font-size="14" text-anchor="middle">14</text>
</svg>
<figcaption>3, with the orange ring, has two children. The smallest of its right subtree, 4 with the green ring, takes its place.</figcaption>
</figure>

```python
def delete(node, value):
    if node is None:
        return None
    if value < node.value:
        node.left = delete(node.left, value)
    elif value > node.value:
        node.right = delete(node.right, value)
    else:
        if node.left is None:              # 1 and 2: at most one child
            return node.right
        if node.right is None:
            return node.left
        successor = minimum(node.right)    # 3: two children
        node.value = successor
        node.right = delete(node.right, successor)
    return node

for v in [7, 14, 3]:
    root = delete(root, v)
    print("delete", v, "->", inorder(root))
print("root:", root.value, "left:", root.left.value)
```

```text
delete 7 -> [1, 3, 4, 6, 8, 10, 13, 14]
delete 14 -> [1, 3, 4, 6, 8, 10, 13]
delete 3 -> [1, 4, 6, 8, 10, 13]
root: 8 left: 4
```

`7` was a leaf, `14` had one child (`13`), `3` had two children: the smallest
of its right subtree, `4`, took its place. After three deletions inorder is
still sorted.

## The insertion order changes everything

When the same values are inserted in a different order, the tree's shape
changes. If the values come **sorted**, each new value goes to the right of
the previous one and the tree turns into a chain:

<figure class="fig">
<svg viewBox="0 0 254 236" width="254" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="161.0" y1="163.0" x2="207.0" y2="209.0"/>
<line class="line" x1="115.0" y1="117.0" x2="161.0" y2="163.0"/>
<line class="line" x1="69.0" y1="71.0" x2="115.0" y2="117.0"/>
<line class="line" x1="23.0" y1="25.0" x2="69.0" y2="71.0"/>
<circle class="box" cx="23.0" cy="25.0" r="17"/>
<text class="ink" x="23.0" y="29.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="69.0" cy="71.0" r="17"/>
<text class="ink" x="69.0" y="75.9" font-size="14" text-anchor="middle">2</text>
<circle class="box" cx="115.0" cy="117.0" r="17"/>
<text class="ink" x="115.0" y="121.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="161.0" cy="163.0" r="17"/>
<text class="ink" x="161.0" y="167.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="207.0" cy="209.0" r="17"/>
<text class="ink" x="207.0" y="213.9" font-size="14" text-anchor="middle">5</text>
</svg>
<figcaption>When 1, 2, 3, 4, 5 are inserted in order, each value lands to the right of the previous one: height 5.</figcaption>
</figure>

We inserted the 2000 numbers from 0 to 1999 in two orders and measured:

```text
mixed  order: height 24 | steps to find 1999: 9
sorted order: height 2000 | steps to find 1999: 2000
```

In mixed order the height is 24, finding `1999` takes 9 steps. In sorted
order the height is 2000: the tree is now a linked list and search is
`O(n)`. This happens often with real data: records arriving by date or
increasing order numbers are already sorted.

## Balanced trees

The fix is to **keep the tree balanced** on every insert and delete. The
**AVL tree** and the **red-black tree** do this with small relinkings called
**rotations**: when one side grows too long, they turn a few links and keep
the height at `O(log n)`. Their code is long and detailed; knowing the idea
is enough here:

- In a balanced BST, search, insert and delete are **always** `O(log n)`.
- Java's `TreeMap` and C++'s `std::map` are usually red-black trees.
- Database indexes (`CREATE INDEX` in the SQL path) work with the version
  developed for disks, the **B-tree**: hundreds of keys in a node, so even
  with millions of rows the tree has only a few levels.

Python's standard library has no balanced tree. When a sorted collection is
needed, a **sorted list + `bisect`** is usually enough: search `O(log n)`,
insert `O(n)` because of the shifting but at C speed. For very large and
frequently changing collections there is the third-party `sortedcontainers`
package.

## In data science: nearest neighbours

k-nearest neighbors (KNN) looks for the examples closest to a point.
Scanning the whole data set is `O(n)` for every prediction. scikit-learn uses
the multi-dimensional version of the BST idea for this: a **k-d tree** splits
left/right by a different feature at each level and rules out far regions
without visiting them. `KNeighborsClassifier(algorithm="kd_tree")` builds
this tree.

## Summary

- The BST rule: the left subtree is smaller, the right subtree larger; for
  the **whole** subtree.
- The inorder walk gives the values sorted.
- Search, insert, delete are `O(h)`. When deleting a node with two children,
  the next value (the smallest of the right subtree) takes its place.
- Values inserted in sorted order make a chain, `h = n`. Balanced trees (AVL,
  red-black) keep `h = O(log n)` with rotations; databases use B-trees.
- In Python a sorted list + `bisect` is enough for most work.
