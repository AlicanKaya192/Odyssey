# Linked Lists

A Python list keeps its elements **side by side** in memory: indexing is
`O(1)`, but adding at the front or in the middle shifts every element,
`O(n)`. A **linked list** makes the opposite choice: the elements are
scattered in memory, and each carries **the address of the next one**. No
shifting; adding at the front is `O(1)`. The price: reaching the `i`-th
element means counting from the start, `O(n)`.

Python has no ready-made linked list class (`deque` uses a similar structure
inside). We will write one ourselves; the real goal is learning to **think in
pointers**: trees and graphs are built on the same idea.

## The node

Each piece of a linked list is a **node**: a value and a **link** to the next
node (`next`). The last node's `next` is `None`. The list itself only holds
the first node (the **head**).

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def to_list(head):                 # walk the nodes into a Python list
    out = []
    while head:
        out.append(head.value)
        head = head.next
    return out

head = Node(1, Node(2, Node(3)))
print(to_list(head))
head = Node(0, head)               # adding at the front: O(1)
print(to_list(head))
```

```text
[1, 2, 3]
[0, 1, 2, 3]
```

<figure class="fig">
  <div class="flow">
    <span class="node acc">head → 0</span><span class="arrow">→</span>
    <span class="node">1</span><span class="arrow">→</span>
    <span class="node">2</span><span class="arrow">→</span>
    <span class="node">3</span><span class="arrow">→</span>
    <span class="node">None</span>
  </div>
  <figcaption>Each node carries a value and a link to the next. The link of 0, added at the front, points to 1, the old head.</figcaption>
</figure>

No element was shifted when adding at the front: the new node points to the
old head, and the list now starts from the new node. Let us measure the
difference; adding 50 000 elements at the front:

```text
linked list, add at front : 9.0 ms
list.insert(0, x)         : 198.5 ms
```

## Walking: `while head:`

A linked list has no index for `for`; you move a pointer from node to node:
`head = head.next`. When `head` becomes `None`, the list is over. This one line
is the skeleton of every linked-list algorithm. Careful: forgetting to move
the pointer is an endless loop.

## Reversing the list

Turning the direction of the links in a single pass is a classic question.
Three pointers are needed: previous (`prev`), current (`head`), next (`nxt`).
You save the next one before losing it:

```python
def reverse(head):
    prev = None
    while head:
        nxt = head.next        # 1. save the next one
        head.next = prev       # 2. turn the arrow back
        prev = head            # 3. step forward
        head = nxt
    return prev               # the new head

print(to_list(reverse(head)))
```

```text
[3, 2, 1, 0]
```

`O(n)` time, `O(1)` extra memory: no new node was built, only the arrows
turned. Order matters: skip step 1 and after step 2 you can no longer reach
the rest of the list.

## Is there a cycle? The tortoise and the hare

If, because of a bug, the last node points back to a node in the middle, the
list is **cyclic** and `while head:` never ends. Keeping the seen nodes in a
set works (`O(n)` memory), but there is a more elegant way: **two pointers**.
One moves one step at a time (the tortoise), the other two at a time (the
hare). With no cycle the hare reaches the end; with a cycle it **must catch
up** with the tortoise inside the cycle (like a fast runner lapping a slow one
on a track).

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:          # the same node (is: identity comparison)
            return True
    return False

a, b, c, d = Node("a"), Node("b"), Node("c"), Node("d")
a.next, b.next, c.next = b, c, d
print(has_cycle(a))
d.next = b                        # d → b: a cycle
print(has_cycle(a))
```

```text
False
True
```

`O(n)` time, `O(1)` memory. It is the two-pointer pattern on a linked list;
the same idea finds the **middle** of the list too (when the hare reaches the
end, the tortoise is in the middle).

## A linked list's real-world job: the LRU cache

A website wants to keep its most requested pages in memory, but space is
limited: when full, it will drop **the one unused for the longest time**. This
is called an **LRU (least recently used) cache**. Two jobs must both be fast:

- Finding by key: `O(1)` → a **dictionary**.
- Keeping the "most recently used" order, moving an element to the end of it,
  dropping the oldest from the front: `O(1)` → a **doubly linked list** (each
  node knows both the previous and the next).

Python's `collections.OrderedDict` is exactly the combination of the two:
inside it there is a dictionary and a doubly linked list. `move_to_end` and
`popitem(last=False)` are linked-list operations, both `O(1)`:

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return None
        self.data.move_to_end(key)          # used: now the newest
        return self.data[key]

    def put(self, key, value):
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)   # drop the oldest

cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
print(cache.get("a"))
cache.put("c", 3)                           # full: the oldest, b, is dropped
print(cache.get("b"), list(cache.data))
```

```text
1
None ['a', 'c']
```

Reading `a` made it the newest; when `c` arrived, `b`, the oldest, was dropped
to make room. Python also has the ready-made `functools.lru_cache` decorator
for caching function results; the same idea runs inside it (we will use it in
the Dynamic Programming section).

## A linked list or a Python list?

<figure class="fig">
  <div class="versus">
    <div><h4>Python list</h4>
      <p><code>items[i]</code>: <code>O(1)</code></p>
      <p>Adding at the front/middle: <code>O(n)</code> (shifting)</p>
      <p>Side by side in memory, cache-friendly</p></div>
    <div class="ok"><h4>Linked list</h4>
      <p>The <code>i</code>-th element: <code>O(n)</code> (counting from the start)</p>
      <p>Adding at the front or after a node you hold: <code>O(1)</code></p>
      <p>Each node is a separate object, extra memory</p></div>
  </div>
  <figcaption>If you often add and remove at the front/middle and hold the node, a linked list; if you index, a Python list.</figcaption>
</figure>

In practice a list or a `deque` is enough for most work in Python; you rarely
write a linked list yourself. But the **node + link** way of thinking is the
foundation of the coming sections: in a tree each node has two children, in a
graph as many neighbours as it likes.

## Summary

- A linked list: each node is a value + a link to the next node; the list
  only holds the head.
- Adding at the front is `O(1)`, reaching the `i`-th element `O(n)`.
- The walking skeleton: `while head: ...; head = head.next`.
- Reversing: three pointers, `O(n)` time, `O(1)` memory.
- Finding a cycle: the tortoise and the hare, `O(1)` memory.
- The LRU cache: a dictionary + a doubly linked list; in Python
  `OrderedDict` and `functools.lru_cache`.
