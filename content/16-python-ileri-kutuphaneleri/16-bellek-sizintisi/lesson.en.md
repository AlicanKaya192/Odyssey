# Memory Leaks

A server uses 200 MB of memory at start-up; a day later 2 GB, a week later the
machine runs out of memory and the program crashes. This is a **memory
leak**: data that is no longer useful stays in memory and piles up. Python
manages memory itself, you never write `free`; so people think "Python cannot
leak". It can, but the cause is different: **a reference that is still held
somewhere**. This section covers how Python frees memory, the typical sources
of leaks, how to find them and how to prevent them.

## Reference counting: when is an object deleted?

```python
import sys
import weakref


class Node:
    def __init__(self, name):
        self.name = name
        self.other = None


a = Node("a")
weakref.finalize(a, print, "freed a")
print(sys.getrefcount(a))
b = a
print(sys.getrefcount(a))
del b
del a
print("after del")
```

```text
2
3
freed a
after del
```

- For every object Python counts **how many places point to it** (the
  reference count). `sys.getrefcount(a)` gives it; the call itself adds a
  temporary reference, so it shows one more.
- `b = a` creates a new **name**, not a new object: the count became 3.
- When the last reference goes too (`del a`), the count drops to zero and the
  object is deleted **at once**: "freed a" was printed before "after del".
- **`weakref.finalize(obj, function, ...)`** registers a function to be called
  when the object is deleted; it does not keep the object alive. In this
  section we use it to see "was it deleted?".

## Cycles and the garbage collector (gc)

```python
import gc
import weakref


class Node:
    def __init__(self, name):
        self.name = name
        self.other = None


gc.disable()
x = Node("x")
y = Node("y")
x.other = y
y.other = x
weakref.finalize(x, print, "freed x")
weakref.finalize(y, print, "freed y")
del x, y
print("names deleted")
found = gc.collect()
print(found >= 2)
gc.enable()
```

```text
names deleted
freed x
freed y
True
```

- `x` points to `y` and `y` to `x`: a **reference cycle**. Even after the
  names are deleted, each count stays at 1 (they point to each other);
  reference counting cannot delete them.
- Python's second mechanism is the **cyclic garbage collector** (`gc`): every
  now and then it scans objects, finds cycles that cannot be reached from
  outside, and deletes them. To see this, we turned automatic collection off
  (`gc.disable()`) and ran it by hand with `gc.collect()`.
- The collector normally runs by itself; so cycles are **eventually**
  deleted. But when it will run is not known, and large cycles hold memory
  until then. A real program does not write `gc.disable()`.

## Leak 1: a cache that grows without limit

```python
import tracemalloc
from functools import lru_cache

tracemalloc.start()
_cache = {}


def handle(request_id):
    result = f"report {request_id} " * 50
    _cache[request_id] = result
    return len(result)


before = tracemalloc.get_traced_memory()[0]
for i in range(10_000):
    handle(i)
grown = (tracemalloc.get_traced_memory()[0] - before) / 1024


@lru_cache(maxsize=100)
def handle_bounded(request_id):
    return f"report {request_id} " * 50


before = tracemalloc.get_traced_memory()[0]
for i in range(10_000):
    handle_bounded(i)
bounded = (tracemalloc.get_traced_memory()[0] - before) / 1024
print(len(_cache), round(grown))
print(handle_bounded.cache_info().currsize, round(bounded))
```

```text
10000 6798
100 80
```

- **This is the most common leak.** Putting every result into a module-level
  dictionary "in case it is needed again": the dictionary never shrinks. If
  every request brings a new key (a user id, a timestamp), it grows for as
  long as the program runs. About 6.8 MB for 10,000 requests; hundreds of MB
  for a million.
- **`tracemalloc`** tracks the memory Python allocates:
  `get_traced_memory()` → `(current, peak)` bytes.
- The fix: put a **limit** on the cache. **`lru_cache(maxsize=100)`** keeps
  the 100 most recently used results and drops the oldest (the functools
  section). Memory stayed at 80 KB.
- The same problem happens with a module-level list (`log_lines.append(...)`),
  with a class attribute (a list shared by all instances) and with
  `lru_cache(maxsize=None)`.

## Leak 2: forgotten listeners

```python
import gc
import weakref


class Bus:
    def __init__(self):
        self.listeners = []

    def subscribe(self, callback):
        self.listeners.append(callback)


class WeakBus:
    def __init__(self):
        self.listeners = []

    def subscribe(self, callback):
        self.listeners.append(weakref.WeakMethod(callback))

    def emit(self, event):
        alive = []
        for ref in self.listeners:
            callback = ref()
            if callback is not None:
                callback(event)
                alive.append(ref)
        self.listeners = alive


class Widget:
    def __init__(self, bus, name):
        weakref.finalize(self, print, "freed", name)
        bus.subscribe(self.on_event)

    def on_event(self, event):
        pass


bus = Bus()
w = Widget(bus, "w1")
del w
gc.collect()
print("strong listeners:", len(bus.listeners))
weak_bus = WeakBus()
w = Widget(weak_bus, "w2")
del w
weak_bus.emit("tick")
print("weak listeners:", len(weak_bus.listeners))
```

```text
strong listeners: 1
freed w2
weak listeners: 0
freed w1
```

- `Widget` registers itself with the event bus: `bus.listeners` now points to
  `self.on_event`, which points to `self`. Deleting the widget is not enough;
  `gc.collect()` cannot delete it either, because this is not a cycle but a
  **reachable** reference. "w1" was only deleted when the program **shut
  down** (the last line).
- UI windows, plug-ins, event listeners and callbacks often leak: the window
  closes but its registration stays.
- Fix 1: **unsubscribe** when closing.
- Fix 2: a **weak reference**. `weakref.WeakMethod` points to the method but
  does not keep the object alive; when the object goes, `ref()` returns
  `None` and the list is cleaned. For plain objects: `weakref.ref`, `WeakSet`,
  `WeakValueDictionary`.
- In the output: "w2" was deleted at `del w`; when the event was sent, the
  dead entry was dropped from the list too (`0`).

## Finding a leak: comparing tracemalloc snapshots

```python
import tracemalloc
from pathlib import Path

tracemalloc.start()
first = tracemalloc.take_snapshot()
kept = [bytearray(1000) for _ in range(2000)]
second = tracemalloc.take_snapshot()
top = second.compare_to(first, "lineno")[0]
frame = top.traceback[0]
print(Path(frame.filename).name, frame.lineno)
print(top.size_diff // 1024 > 1900)
tracemalloc.stop()
```

```text
main.py 6
True
```

- **`take_snapshot()`** takes a picture of all allocations at that moment.
  Comparing two pictures with **`compare_to(earlier, "lineno")`** sorts the
  memory growth **line by line**, largest first.
- The first line is where the code holding the memory is: line 6 (where the
  list is built), about 2 MB.
- In a long-running program: take a snapshot at intervals and look for the
  line that keeps growing near the top. (The notes have a full example.)
- `tracemalloc` sees allocations **reported to Python**. Memory some libraries
  allocate on their C side may not show up; pandas' Arrow-based columns are
  like that (measured in the Big Data path).

## Other sources

| Source | What happens | Prevention |
|---|---|---|
| A file / connection never closed | an operating system resource stays open | `with` |
| Clean-up with `__del__` | it is unknown when it will run | `with` and a context manager (the contextlib section) |
| A closure | an inner function captures a big object | capture only what you need |
| A stored exception | the exception holds every frame through `__traceback__` | do not keep exceptions long; keep only the message |
| A thread that never ends | it keeps living with its data | a stop signal, `join` |
| Jupyter | every output stays in `Out[n]` and `_` variables | `del` + `gc.collect()`, restart the kernel |

About `__del__`: since Python 3.4, objects with `__del__` are collected in
cycles too; the real problem is that the timing is uncertain. Releasing
resources such as files, locks and connections is guaranteed with `with`.

## Summary

- Python deletes an object at once when its reference count drops to zero;
  `gc` collects cycles every now and then.
- A leak = data that is useless but still **reachable**: a growing cache, a
  forgotten listener, a stored exception.
- A limit on caches (`lru_cache(maxsize=...)`), weak references for listeners
  or unsubscribing.
- `tracemalloc`: `get_traced_memory`, `take_snapshot`, `compare_to`.
- Confirm an object was really deleted with `weakref.finalize`.
