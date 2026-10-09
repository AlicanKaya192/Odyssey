## Caching

| Code | What it does |
|---|---|
| `@lru_cache(maxsize=128)` | store the 128 most recently used results |
| `@lru_cache(maxsize=None)` / `@cache` | store without limit |
| `f.cache_info()` | hits, misses, size |
| `f.cache_clear()` | empty the cache |
| `@cached_property` | compute a property once, store it on the object |

Only for functions that always give the same result for the same input; the
arguments must be immutable (hashable).

## Producing functions

| Code | What it gives |
|---|---|
| `partial(f, a, b=2)` | a new function with arguments fixed |
| `reduce(f, seq, start)` | reducing to one value from left to right |
| `operator.add`, `mul`, `itemgetter("name")` | operators as functions |

## Decorators

| Code | What it does |
|---|---|
| `@wraps(func)` | copies the real name and description onto the wrapper |
| `@total_ordering` | all comparisons from `__eq__` + `__lt__` |
| `@singledispatch` + `.register` | a version per type of the first argument |

## A decorator skeleton

```python
from functools import wraps


def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper
```
