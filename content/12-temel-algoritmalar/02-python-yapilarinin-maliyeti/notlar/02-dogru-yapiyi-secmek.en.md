Which structure to use in a problem is often decided by **the question you
will ask most often**.

| Most frequent question / job | Structure | Why |
|---|---|---|
| "What is element i?" | `list` | `O(1)` by index |
| "Add to the end, go through in order" | `list` | `append` amortised `O(1)` |
| "Has this value been seen before?" | `set` | `in` `O(1)` on average |
| "What is this key's value?" (counter, mapping) | `dict` | `O(1)` on average |
| "First in, first out" (queue) | `collections.deque` | `popleft` `O(1)` |
| "Last in, first out" (stack) | `list` (`append` + `pop`) | `O(1)` at the end |
| "Always give me the smallest/largest" | `heapq` | in the Priority Queues section |
| "Keep it sorted, search in it" | a sorted `list` + `bisect` | in the Searching section |

## Examples: which structure?

**1. The names of users logging in to a site today arrive; at every new
login we will ask "is this their first visit today?".**
→ `set`. With a list we would scan the whole list at every login.

**2. We will count how many times every word occurs in a list of words.**
→ `dict` (or `collections.Counter`). Calling `items.count(w)` for every word
would be `O(n²)`.

**3. Jobs arrive at a printer in order; the first in is printed first.**
→ `deque`. `pop(0)` on a list shifts the whole list every time.

**4. A list is often asked for "the record at position 75".**
→ `list`. A set keeps no order, and reaching the middle of a `deque` is
slow.

## Using two structures together

Sometimes one structure is not enough: for "remove the repeats but **keep
the order**", a **list** is kept for the order and a **set** for the "seen
it?" question. That is exactly what `unique_with_set` was in the lesson. The
extra memory is `O(n)`; in return `O(n²)` work drops to `O(n)`.

Note: since Python 3.7 a `dict` keeps insertion order, so
`list(dict.fromkeys(items))` also removes repeats while keeping the order.
