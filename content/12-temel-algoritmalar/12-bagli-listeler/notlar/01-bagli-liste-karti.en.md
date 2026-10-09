## Costs

| Operation | Singly linked list | Python list |
|---|---|---|
| Add / delete at the front | `O(1)` | `O(n)` |
| Add at the end | `O(n)` (`O(1)` if the tail is kept) | `O(1)` amortised |
| The `i`-th element | `O(n)` | `O(1)` |
| Searching for a value | `O(n)` | `O(n)` |
| Adding after a node you hold | `O(1)` | `O(n)` |

## Singly and doubly linked

- **Singly:** a node only knows its `next`. To delete a node you need to find
  **the one before** it.
- **Doubly:** a node knows `prev` and `next`. You can delete any node you hold
  in `O(1)`: `node.prev.next = node.next`, `node.next.prev = node.prev`. That
  is why an LRU cache wants a doubly linked list.

## The sentinel node

Cases like an empty list or "deleting the first node" need separate `if`s.
Putting a **dummy node** at the front, whose value does not matter and which
always exists, removes those special cases:

```python
dummy = Node(None, head)     # the dummy node at the front
prev = dummy
while prev.next:
    if prev.next.value == target:
        prev.next = prev.next.next     # the first node is deleted by the same code
        break
    prev = prev.next
head = dummy.next
```

## Common mistakes

- Forgetting to move the pointer (`head = head.next`) → an endless loop.
- Not saving the next one before changing a link → the rest of the list is
  lost.
- Reaching `.next` of `None` → `AttributeError`. Write the loop condition like
  `while node and node.next:`.
- Mixing up equality and identity: `is` when comparing nodes, `==` when
  comparing values.
