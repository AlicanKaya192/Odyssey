# Trees

The folders on your computer, the HTML of a web page, a company's
organisation chart: all of them are **hierarchies**. One on top, a few below
it, and more below those. This structure is called a **tree**.

In a linked list each node had a single "next". In a tree a node can have
**several children**. You will meet trees often in data science too: decision
trees, random forests and gradient boosting models are all trees.

## Terms

<figure class="fig">
<svg viewBox="0 0 350 180" width="350" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="79.0" y1="89.0" x2="23.0" y2="153.0"/>
<line class="line" x1="79.0" y1="89.0" x2="135.0" y2="153.0"/>
<line class="line" x1="247.0" y1="89.0" x2="303.0" y2="153.0"/>
<line class="line" x1="191.0" y1="25.0" x2="79.0" y2="89.0"/>
<line class="line" x1="191.0" y1="25.0" x2="247.0" y2="89.0"/>
<circle class="box" cx="23.0" cy="153.0" r="17"/>
<circle class="curve4" cx="23.0" cy="153.0" r="17"/>
<text class="ink" x="23.0" y="157.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="79.0" cy="89.0" r="17"/>
<text class="ink" x="79.0" y="93.9" font-size="14" text-anchor="middle">2</text>
<circle class="box" cx="135.0" cy="153.0" r="17"/>
<circle class="curve4" cx="135.0" cy="153.0" r="17"/>
<text class="ink" x="135.0" y="157.9" font-size="14" text-anchor="middle">5</text>
<circle class="box" cx="191.0" cy="25.0" r="17"/>
<circle class="curve" cx="191.0" cy="25.0" r="17"/>
<text class="ink" x="191.0" y="29.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="247.0" cy="89.0" r="17"/>
<text class="ink" x="247.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="303.0" cy="153.0" r="17"/>
<circle class="curve4" cx="303.0" cy="153.0" r="17"/>
<text class="ink" x="303.0" y="157.9" font-size="14" text-anchor="middle">6</text>
</svg>
<figcaption>The purple ring is the root, the green rings are the leaves. 2, 4 and 5 together form a subtree.</figcaption>
</figure>

- **Root:** the top node, with no parent. Here `1`.
- **Parent and child:** `2` is the parent of `4` and `5`; `4` and `5` are
  the children of `2`.
- **Leaf:** a node with no children. Here `4`, `5`, `6`.
- **Subtree:** a node and everything below it. `2`, `4`, `5` form a subtree;
  it is a tree itself.
- **Depth:** a node's distance from the root (the root is 0). **Height:** the
  number of nodes on the longest path from the root to a leaf; 3 in this tree.

If every node has **at most two** children, the tree is a **binary tree**;
the children are called **left** and **right**. In this section we will work
with binary trees.

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

root = TreeNode(1,
                TreeNode(2, TreeNode(4), TreeNode(5)),
                TreeNode(3, None, TreeNode(6)))
```

The same as the linked list's `Node`, only with `left` and `right` instead of
`next`. A missing child is `None`.

## Recursion is the natural language of trees

The definition of a tree contains itself: a tree is either **empty** or a root
and **two subtrees**. The pattern from the Recursion section fits exactly:

- **Base case:** the empty tree (`None`).
- **Recursive step:** take the answer from the two children and combine it
  with your own node.

```python
def size(node):                    # number of nodes
    if node is None:
        return 0
    return 1 + size(node.left) + size(node.right)

def height(node):                  # height
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))

print(size(root), height(root))
```

```text
6 3
```

Both visit every node once: `O(n)`. Most tree problems are solved with this
two-line skeleton; only the "combine" part changes (a sum, the largest, a
counter…).

## Depth-first walks: three orders

There are three classic orders for walking all the nodes. The difference is
whether the node itself is written **before, between or after** its
children:

```python
def preorder(node):                # root first, then left, then right
    if node is None:
        return []
    return [node.value] + preorder(node.left) + preorder(node.right)

def inorder(node):                 # left, root, right
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)

def postorder(node):               # left, right, root last
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.value]

print("preorder :", preorder(root))
print("inorder  :", inorder(root))
print("postorder:", postorder(root))
```

```text
preorder : [1, 2, 4, 5, 3, 6]
inorder  : [4, 2, 5, 1, 3, 6]
postorder: [4, 5, 2, 6, 3, 1]
```

Each is good for something:

- **Preorder (root first):** copying or printing the structure top-down (like
  listing a folder tree with indentation).
- **Inorder (root in the middle):** in the **binary search tree** of the next
  section it gives the values **sorted**.
- **Postorder (root last):** when the children's answers are needed first; a
  folder's size cannot be computed without the sizes of what is inside.

All three go down one path **to the bottom**, then come back. That is why
they are all called **depth-first search (DFS)**.

## Breadth-first walk: level by level

Sometimes you want to read the tree floor by floor: first the root, then its
children, then the grandchildren. This is called **breadth-first search
(BFS)** and its tool is the **queue** from the Stacks and Queues section:
first in, first processed.

<figure class="fig">
<svg viewBox="0 0 424 180" width="424" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="30" font-size="12">level 0</text>
<text class="dim" x="4" y="94" font-size="12">level 1</text>
<text class="dim" x="4" y="158" font-size="12">level 2</text>
<line class="line" x1="153.0" y1="89.0" x2="97.0" y2="153.0"/>
<line class="line" x1="153.0" y1="89.0" x2="209.0" y2="153.0"/>
<line class="line" x1="321.0" y1="89.0" x2="377.0" y2="153.0"/>
<line class="line" x1="265.0" y1="25.0" x2="153.0" y2="89.0"/>
<line class="line" x1="265.0" y1="25.0" x2="321.0" y2="89.0"/>
<circle class="box" cx="97.0" cy="153.0" r="17"/>
<text class="ink" x="97.0" y="157.9" font-size="14" text-anchor="middle">4</text>
<circle class="box" cx="153.0" cy="89.0" r="17"/>
<text class="ink" x="153.0" y="93.9" font-size="14" text-anchor="middle">2</text>
<circle class="box" cx="209.0" cy="153.0" r="17"/>
<text class="ink" x="209.0" y="157.9" font-size="14" text-anchor="middle">5</text>
<circle class="box" cx="265.0" cy="25.0" r="17"/>
<text class="ink" x="265.0" y="29.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="321.0" cy="89.0" r="17"/>
<text class="ink" x="321.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="377.0" cy="153.0" r="17"/>
<text class="ink" x="377.0" y="157.9" font-size="14" text-anchor="middle">6</text>
</svg>
<figcaption>BFS reads level 0 first, then level 1, then level 2, left to right.</figcaption>
</figure>

```python
from collections import deque

def level_order(root):
    if root is None:
        return []
    levels = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):        # what is in the queue now = this level
            node = queue.popleft()
            level.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels

print(level_order(root))
```

```text
[[1], [2, 3], [4, 5, 6]]
```

The trick is `for _ in range(len(queue))`: when the inner loop starts, the
queue holds **only this level's** nodes; their children are added to the back
of the queue and handled in the next round.

## DFS without recursion: with a stack

With recursion Python kept the call stack. You can do the same job yourself
with an explicit **stack**:

```python
def preorder_iter(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.value)
        if node.right:                 # right first: it comes out last
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out

print(preorder_iter(root))
```

```text
[1, 2, 4, 5, 3, 6]
```

The result is the same as the recursive `preorder`. A queue gives BFS, a stack
gives DFS: the only difference between the two walks is which end you take
from. The two will meet us again in the Graphs section.

## Why does height matter?

Most work in a tree walks from the root towards a leaf; the cost is the
**height (`h`)**. The same number of nodes can be arranged at two very
different heights:

```text
balanced: 511 nodes, height 9
chain   : 511 nodes, height 511
chain of 5000 nodes: RecursionError
```

Arranged **balanced**, 511 nodes have height 9: each level holds twice as
many nodes as the one before, `h ≈ log₂ n`. If every node has a single child,
the tree is really a linked list, `h = n`. There is a practical price too: on
a chain of 5000 nodes the recursive `height` hit Python's recursion limit
(`RecursionError`). In the next section we will see why keeping a tree
balanced matters so much.

## A tree in data science: the decision tree

A **decision tree** asks a question at each inner node ("is the petal length
at most 2.5?"), goes left or right depending on the answer, and writes the
prediction in the leaf. The small tree below splits iris flowers into three
species:

<figure class="fig">
<svg viewBox="0 0 575 180" width="575" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="370.6" y1="89.0" x2="275.6" y2="153.0"/>
<text class="dim" x="313.1" y="121.0" font-size="12" text-anchor="end">yes</text>
<line class="line" x1="370.6" y1="89.0" x2="465.6" y2="153.0"/>
<text class="dim" x="428.1" y="121.0" font-size="12" text-anchor="start">no</text>
<line class="line" x1="180.6" y1="25.0" x2="85.6" y2="89.0"/>
<text class="dim" x="123.1" y="57.0" font-size="12" text-anchor="end">yes</text>
<line class="line" x1="180.6" y1="25.0" x2="370.6" y2="89.0"/>
<text class="dim" x="285.6" y="57.0" font-size="12" text-anchor="start">no</text>
<rect class="box" x="53.0" y="72.0" width="65.0" height="34" rx="8"/>
<rect class="curve4" x="53.0" y="72.0" width="65.0" height="34" rx="8"/>
<text class="ink" x="85.6" y="93.9" font-size="14" text-anchor="middle">setosa</text>
<rect class="box" x="101.0" y="8.0" width="159.1" height="34" rx="8"/>
<text class="ink" x="180.6" y="29.9" font-size="14" text-anchor="middle">petal_length ≤ 2.5</text>
<rect class="box" x="227.4" y="136.0" width="96.4" height="34" rx="8"/>
<rect class="curve4" x="227.4" y="136.0" width="96.4" height="34" rx="8"/>
<text class="ink" x="275.6" y="157.9" font-size="14" text-anchor="middle">versicolor</text>
<rect class="box" x="291.0" y="72.0" width="159.1" height="34" rx="8"/>
<text class="ink" x="370.6" y="93.9" font-size="14" text-anchor="middle">petal_width ≤ 1.75</text>
<rect class="box" x="421.3" y="136.0" width="88.6" height="34" rx="8"/>
<rect class="curve4" x="421.3" y="136.0" width="88.6" height="34" rx="8"/>
<text class="ink" x="465.6" y="157.9" font-size="14" text-anchor="middle">virginica</text>
</svg>
<figcaption>Inner nodes ask questions, the leaves with green rings give the prediction. Left if yes, right if no.</figcaption>
</figure>

We can keep the tree as nested dictionaries; predicting is walking from the
root to a leaf:

```python
tree = {
    "feature": "petal_length", "threshold": 2.5,
    "left": "setosa",
    "right": {
        "feature": "petal_width", "threshold": 1.75,
        "left": "versicolor",
        "right": "virginica",
    },
}

def predict(node, flower):
    while isinstance(node, dict):          # a leaf is a string
        if flower[node["feature"]] <= node["threshold"]:
            node = node["left"]
        else:
            node = node["right"]
    return node

print(predict(tree, {"petal_length": 1.4, "petal_width": 0.2}))
print(predict(tree, {"petal_length": 4.5, "petal_width": 1.5}))
print(predict(tree, {"petal_length": 5.8, "petal_width": 2.2}))
```

```text
setosa
versicolor
virginica
```

scikit-learn's `DecisionTreeClassifier` does exactly this when predicting;
the cost is the tree's **depth**, independent of the size of the data set.
We will build how the tree picks its questions from the data from scratch in
ALG 3.

## Summary

- A tree: a hierarchy; root, child, leaf, subtree. In a binary tree, at most
  two children.
- The recursive skeleton: if `None`, the base case; otherwise combine the two
  children's answers. `O(n)`.
- DFS: preorder (root first), inorder (in the middle), postorder (last); it
  can also be written without recursion using a stack.
- BFS: level by level with a queue; `for _ in range(len(queue))` separates one
  level.
- Root-to-leaf work is `O(h)`: `h ≈ log₂ n` in a balanced tree, `h = n` in a
  chain.
- Prediction in a decision tree is one walk from the root to a leaf.
