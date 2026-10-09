## Operations

| Job | Stack (`list`) | Queue (`collections.deque`) |
|---|---|---|
| Add | `stack.append(x)` `O(1)` | `queue.append(x)` `O(1)` |
| Take | `stack.pop()` `O(1)` | `queue.popleft()` `O(1)` |
| Look without taking | `stack[-1]` | `queue[0]` |
| Empty? | `if not stack:` | `if not queue:` |
| Size | `len(stack)` | `len(queue)` |

## Common mistakes

- **Taking from an empty structure:** `[].pop()` and `deque().popleft()` raise
  `IndexError`. Check `if stack:` before taking.
- **Making a queue with a list:** `items.pop(0)` shifts the whole list every
  time: as the queue grows it heads towards `O(n²)`.
- **Order in postfix:** the operand popped first is the **right** one:
  `right = pop()`, then `left = pop()`. It does not matter for addition and
  multiplication; it does for subtraction and division.

## Which one when?

| Question | Structure |
|---|---|
| "The last one opened/added must close first" | stack |
| "Undo" / "go back one step" | stack |
| "First come, first processed" | queue |
| "Near to far, level by level" (BFS) | queue |
| "Dive deep, then come back" (DFS) | stack (or recursion) |
| "The next greater/smaller element" | monotonic stack |
| "Always give me the smallest/largest" | priority queue (`heapq`, section 15 of this module) |

## Between threads

If several threads will write to and read from the same queue, use
`queue.Queue` (FIFO) and `queue.LifoQueue` (stack): locking is done for you.
In a single thread `deque` is faster and enough.
