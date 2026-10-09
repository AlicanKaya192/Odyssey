A decorator means "the same extra job on every function": a counter, timing,
logging, retrying. Two patterns cover most jobs.

## A counter and a retry

```python
from functools import wraps


def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@count_calls
def add(a, b):
    return a + b


add(1, 2)
add(3, 4)
print(add.calls, add.__name__)


def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError as error:
                    print(f"attempt {attempt} failed: {error}")
            raise RuntimeError("giving up")
        return wrapper
    return decorator


answers = iter(["x", "y", "42"])


@retry(times=3)
def read_number():
    return int(next(answers))


print(read_number())
```

```text
2 add
attempt 1 failed: invalid literal for int() with base 10: 'x'
attempt 2 failed: invalid literal for int() with base 10: 'y'
42
```

- **`count_calls`**: on every call the wrapper increases the counter and calls
  the real function. Functions are objects too; they can carry an attribute
  like `wrapper.calls`.
- Thanks to `@wraps(func)`, `add.__name__` is still `add`.

## How a decorator with arguments works

Writing `@retry(times=3)` first calls `retry(times=3)`, which returns **the
real decorator**; that one wraps the function. That is why there are three
nested functions:

| Level | What it takes | What it returns |
|---|---|---|
| `retry(times)` | a setting | the decorator |
| `decorator(func)` | the function | the wrapper |
| `wrapper(*args, **kwargs)` | the call's arguments | the result |

In the example the first two attempts failed because of `int("x")` and
`int("y")`, and `42` came on the third. Had all attempts failed, a
`RuntimeError` would have been raised.

## When a decorator?

- When the same extra job repeats in many functions (measuring, logging,
  checking).
- When the real function's code should not have to know about that job.

Do not write a decorator for something used in one place; a plain function
call is clearer. Most ready-made decorators (`lru_cache`, `property`,
`staticmethod`, `dataclass`) already use this pattern.
