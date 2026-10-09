# functools

This module covers the side of the standard library that pays off in
growing programs. The first stop is **`functools`**: tools that work on
functions. Making a function remember its results (a cache), fixing some of
its arguments in advance, reducing a list to a single value, and wrapping
functions with **decorators**.

## lru_cache: remembering the result

```python
from functools import lru_cache

calls = 0


def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(25), calls)
calls = 0


@lru_cache(maxsize=None)
def fast_fib(n):
    global calls
    calls += 1
    return n if n < 2 else fast_fib(n - 1) + fast_fib(n - 2)


print(fast_fib(25), calls)
print(fast_fib.cache_info())
print(fast_fib(100))
```

```text
75025 242785
75025 26
CacheInfo(hits=23, misses=26, maxsize=None, currsize=26)
354224848179261915075
```

- The recursive `fib(25)` computes the same values again and again:
  **242,785 calls**.
- **`@lru_cache`** stores the function's result for each argument; on a
  second call with the same argument it returns it without computing. The
  same result came with **26 calls**, and `fib(100)` came instantly.
- **`cache_info()`** is the cache's report card: `hits` (served from the
  cache), `misses` (computed), `currsize` (the number of stored results).
- `maxsize=None` stores without limit; given a number, it drops the one used
  least recently (LRU: least recently used).

A cache is only correct for functions that **always give the same result
for the same input**: storing the result of a function that reads a file,
looks at the clock or draws a random number returns a stale result.

## What is a decorator?

`@lru_cache` is a **decorator**: a function that takes a function and returns
a new function wrapping it. Writing `@name` is the same as writing
`f = name(f)` right after the definition.

```python
from functools import wraps


def shout(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


def polite(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + ", please"
    return wrapper


@shout
def greet(name):
    """Return a greeting."""
    return f"hello, {name}"


@polite
def ask(thing):
    """Ask for a thing."""
    return f"pass the {thing}"


print(greet("ada"))
print(greet.__name__, greet.__doc__)
print(ask("salt"))
print(ask.__name__, ask.__doc__)
```

```text
HELLO, ADA
wrapper None
pass the salt, please
ask Ask for a thing.
```

- `wrapper` calls the real function and changes its result; `*args,
  **kwargs` passes every argument through as it is.
- The wrapped `greet` is now `wrapper`: its name is `wrapper` and its
  description is gone. The wrong name shows up in error messages and
  documentation.
- **`@wraps(func)`** copies the real function's name and description onto the
  wrapper. Always use it when writing your own decorator.

Decorators are used for "the same extra job on every function": logging,
timing, checking permissions, retrying; the second note shows this.

## partial and reduce

```python
import operator
from functools import partial, reduce


def power(base, exponent):
    return base ** exponent


square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(square(5), cube(2), list(map(square, [1, 2, 3])))
from_binary = partial(int, base=2)
print(from_binary("1010"), from_binary("11111111"))
print(reduce(operator.mul, [1, 2, 3, 4, 5]))
print(reduce(lambda a, b: a if a > b else b, [3, 9, 2]))
print(reduce(operator.add, [], 0))
```

```text
25 8 [1, 4, 9]
10 255
120
9
0
```

- **`partial(f, ...)`** produces a new function with some arguments filled in
  advance: `square` is `power` with the exponent fixed to 2. Useful when a
  function must be given to `map`, a button or a sort with a **single
  argument**.
- **`reduce(f, seq)`** reduces a sequence to one value from left to right:
  `((((1×2)×3)×4)×5) = 120`. The third argument is the starting value; on an
  empty sequence it raises an error without one.
- The **`operator`** module gives the function form of operators like `+`
  and `*` (`operator.mul`), so no `lambda` is needed. For a total there is
  already `sum`, for the largest `max`; `reduce` is for more special
  accumulations.

## For classes: cached_property and total_ordering

```python
from functools import cached_property, total_ordering


class Report:
    def __init__(self, values):
        self.values = values
        self.computed = 0

    @cached_property
    def total(self):
        self.computed += 1
        return sum(self.values)


r = Report([1, 2, 3])
print(r.total, r.total, r.computed)


@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major, self.minor = major, minor

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)


a, b = Version(1, 2), Version(1, 10)
print(a < b, a >= b, a != b, max(a, b).minor)
```

```text
6 6 1
True False True 10
```

- **`@cached_property`**: the property is computed on first read and stored
  on the object; `r.total` was read twice, computed once.
- **`@total_ordering`**: writing `__eq__` and `__lt__` is enough; `<=`, `>`,
  `>=` come by themselves. `max` and `sorted` work too now. `1.2 < 1.10` is
  right in version order: the tuple comparison is `2 < 10`.

## singledispatch: behaving by type

```python
from functools import singledispatch


@singledispatch
def describe(value):
    return f"something: {value!r}"


@describe.register
def _(value: int):
    return f"integer {value}"


@describe.register
def _(value: list):
    return f"list of {len(value)}"


print(describe(5))
print(describe([1, 2]))
print(describe("hi"))
print(describe(True))
```

```text
integer 5
list of 2
something: 'hi'
integer True
```

**`@singledispatch`** runs a different version of the same-named function
depending on the **type** of the first argument; versions are registered with
a type hint (`value: int`). Instead of a long `if isinstance(...)` chain, each
type lives in its own function. `True` came out as "integer": `bool` is a
subtype of `int`.

## Common mistakes

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def total(items):
    return sum(items)


try:
    total([1, 2])
except TypeError as error:
    print("TypeError:", error)
print(total((1, 2)))


@lru_cache(maxsize=2)
def square(n):
    return n * n


for n in [1, 2, 3, 1]:
    square(n)
print(square.cache_info())
```

```text
TypeError: unhashable type: 'list'
3
CacheInfo(hits=0, misses=4, maxsize=2, currsize=2)
```

- The cache stores arguments as dictionary keys; it does not accept
  **mutable arguments** like lists. Use a tuple.
- With `maxsize=2`, 1 was dropped when 3 came; the next `square(1)` was
  computed again (4 misses, 0 hits). If the cache is too small, the gain is
  lost.
- `maxsize=None` has no limit: the cache of a function called with millions
  of different arguments **fills memory**. That is one of the examples in this
  module's memory leak section.

## Summary

- `@lru_cache(maxsize=...)`: store the results of a function that gives the
  same result for the same input; `cache_info()`, `cache_clear()`.
- A decorator = a function wrapping a function; in your own, `@wraps(func)`.
- `partial` fixes arguments, `reduce` reduces a sequence to one value,
  `operator` is the function form of operators.
- `@cached_property`, `@total_ordering`, `@singledispatch`.
