# Overall Review

You have reached the end of the Python Libraries: Advanced module. You now
know the tools needed to write a program that does not just work but can
**grow**: explicit types and record classes, logging and the command line,
databases and serialisation, correct money calculations and security,
concurrency, tests, measurement and memory. This section walks the path once
more; at the end there is an example where the tools work together.

<figure class="fig">
  <div class="flow">
    <span class="node">Clear code<br><small>00–05</small></span><span class="arrow">→</span>
    <span class="node">Programs<br><small>06–09</small></span><span class="arrow">→</span>
    <span class="node">Maths<br><small>10–11</small></span><span class="arrow">→</span>
    <span class="node">Concurrency<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Robustness<br><small>14–16</small></span>
  </div>
  <figcaption>The module's path: the code itself first, then the program's outside world, finally speed and robustness.</figcaption>
</figure>

## 1. Writing clear code (Sections 0–5)

| Task | Tool |
|---|---|
| Remembering results | `@lru_cache(maxsize=...)`, `@cache` |
| Fixing an argument | `functools.partial` |
| Writing a decorator | an inner function + `@functools.wraps` |
| A sort key | `key=operator.itemgetter(...)`, `attrgetter`, a tuple for several keys |
| The smallest / largest N | `heapq.nsmallest`, `nlargest`; inserting into a sorted list `bisect.insort` |
| Type hints | `list[int]`, <code>X &#124; None</code>, `Literal`, `Callable`, `TypedDict` |
| A record class | `@dataclass`, `field(default_factory=list)`, `frozen=True`, `asdict` |
| A shared interface | `abc.ABC` + `@abstractmethod`; structural `typing.Protocol` |
| Your own `with` block | `@contextmanager` + `yield`; `closing`, `suppress`, `ExitStack` |

A mutable default (`[]`) is not written directly; `lru_cache` arguments must be
hashable; type hints are not checked at run time.

## 2. Real programs (Sections 6–9)

| Task | Tool |
|---|---|
| Keeping logs | `logging.getLogger(__name__)`, levels, `basicConfig`, a handler + format |
| Logging with an error | `log.exception(...)` (traceback included) |
| The command line | `argparse.ArgumentParser`, positional / optional, `type=`, `choices=`, subcommands |
| A database in a file | `sqlite3.connect`, the `?` placeholder, a `with conn:` transaction, `Row` |
| For speed | `executemany`, `CREATE INDEX`, `EXPLAIN QUERY PLAN` |
| Storing a Python object | `pickle.dump` / `load` (`"wb"` / `"rb"`), `shelve` |

`logging` instead of `print`; never put values into SQL by formatting; never
load untrusted pickle data.

## 3. Maths and security (Sections 10–11)

| Task | Tool |
|---|---|
| Money | `Decimal("19.99")`, `quantize(Decimal("0.01"), rounding=...)` |
| An exact fraction | `Fraction(1, 3)`, `limit_denominator` |
| A fingerprint | `hashlib.sha256(data).hexdigest()`, `file_digest` |
| Storing passwords | a salt + `pbkdf2_hmac` / `scrypt`, `hmac.compare_digest` |
| A signature | `hmac.new(key, message, hashlib.sha256)` |
| Secure randomness | `secrets.token_urlsafe`, `token_hex`, `choice` |

A Decimal is built from a string and does not mix with float; when splitting
money, the leftover cent is handed out; for security, `secrets`, not `random`.

## 4. Concurrency (Sections 12–13)

| Task | Tool |
|---|---|
| Network / disk waits | `ThreadPoolExecutor` + `map` / `submit` |
| CPU-heavy work | `ProcessPoolExecutor` + `if __name__ == "__main__":` |
| Shared data | `threading.Lock`, `queue.Queue` |
| Many network waits | `asyncio`: `async def`, `await`, `gather`, `TaskGroup` |
| Time limit, concurrency limit | `asyncio.timeout`, `Semaphore` |
| A blocking call inside async | `asyncio.to_thread` |

`future.result()` raises the job's error; `time.sleep` inside `async def`
stops the event loop.

## 5. Robust code (Sections 14–16)

| Task | Tool |
|---|---|
| Tests | `unittest.TestCase`, `assertEqual`, `assertRaises`, `setUp`, `subTest` |
| Faking the outside world | `unittest.mock.patch` |
| Examples in documentation | `doctest` |
| Measuring a small piece | `min(timeit.repeat(...))` |
| Where the time goes | `cProfile` + `pstats` |
| Memory | `tracemalloc` (`take_snapshot`, `compare_to`), `weakref`, `gc` |

Measure first, then fix; tests cover edge cases; a limit on caches, weak
references for listeners.

## All together

A small program that reads orders from SQLite, turns them into dataclasses,
computes tax with `Decimal` in a thread pool and keeps a log.

```python
import io
import logging
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

stream = io.StringIO()
FORMAT = "%(levelname)s %(name)s %(message)s"
logging.basicConfig(stream=stream, level=logging.INFO, format=FORMAT)
log = logging.getLogger("shop")
CENT = Decimal("0.01")
SCHEMA = "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT, total TEXT)"


@dataclass(frozen=True)
class Order:
    id: int
    customer: str
    total: Decimal


def load(conn: sqlite3.Connection) -> list[Order]:
    rows = conn.execute("SELECT id, customer, total FROM orders ORDER BY id")
    return [Order(i, c, Decimal(t)) for i, c, t in rows]


def with_tax(order: Order) -> Decimal:
    return (order.total * Decimal("1.20")).quantize(CENT, rounding=ROUND_HALF_UP)


with closing(sqlite3.connect(":memory:")) as conn:
    with conn:
        conn.execute(SCHEMA)
        conn.executemany("INSERT INTO orders (customer, total) VALUES (?, ?)",
                         [("ada", "19.99"), ("alan", "5.01"), ("ada", "0.10")])
    orders = load(conn)
log.info("loaded %d orders", len(orders))
with ThreadPoolExecutor(max_workers=3) as pool:
    gross = list(pool.map(with_tax, orders))
print(orders[0])
print([str(g) for g in gross], sum(gross))
print(stream.getvalue().strip())
```

```text
Order(id=1, customer='ada', total=Decimal('19.99'))
['23.99', '6.01', '0.12'] 30.12
INFO shop loaded 3 orders
```

- **sqlite3:** the table is created in a transaction (`with conn:`), values go
  in with `?`, and the connection is closed with `closing` (contextlib).
- **dataclasses + typing:** every row is an immutable (`frozen`) `Order`; the
  functions are documented with their types.
- **decimal:** the amount is text in the database and a `Decimal` in the
  program; tax is rounded to cents "five goes up". No float anywhere.
- **concurrent.futures:** each order's tax is computed in the pool; results in
  order.
- **logging:** the program says what it did with a log, not `print`.

## Common mistakes

| Mistake | The right way |
|---|---|
| `def f(items=[])` | `items=None` or `field(default_factory=list)` |
| `lru_cache(maxsize=None)` with unlimited data | give a `maxsize` |
| Forgetting `wraps` in a decorator | `@functools.wraps(func)` |
| Debugging with `print` | `logging` |
| `f"... WHERE name = '{name}'"` | the `?` placeholder |
| Loading pickle from the internet | JSON |
| `Decimal(0.1)` | `Decimal("0.1")` |
| Storing passwords with `sha256` | a salt + `pbkdf2_hmac` |
| Producing security codes with `random` | `secrets` |
| Increasing a shared counter without a lock | `with lock:` |
| `time.sleep` inside `async def` | `await asyncio.sleep` / `to_thread` |
| Only a "happy path" test | edge cases |
| Speeding up without measuring | `cProfile`, `timeit` |
| A module dictionary that grows forever | a limit, `lru_cache(maxsize=...)` |
