## Fonksiyonlar ve sıralama

```python
from functools import lru_cache, partial, wraps
from operator import itemgetter
import heapq, bisect

@lru_cache(maxsize=256)
def slow(x): ...

rows.sort(key=itemgetter("city", "age"))
heapq.nlargest(3, scores)
bisect.insort(sorted_list, value)
```

## Tipler ve kayıt sınıfları

```python
from dataclasses import dataclass, field
from typing import Literal, Protocol

@dataclass(frozen=True)
class Point:
    x: float
    y: float
    tags: list[str] = field(default_factory=list)

class Drawable(Protocol):
    def draw(self) -> str: ...
```

## Kaynak yönetimi

```python
from contextlib import contextmanager, closing, suppress

@contextmanager
def opened(path):
    f = open(path, encoding="utf-8")
    try:
        yield f
    finally:
        f.close()
```

## Kayıt, komut satırı, veritabanı

```python
import logging, argparse, sqlite3
log = logging.getLogger(__name__)
parser = argparse.ArgumentParser(prog="tool")
parser.add_argument("path")
parser.add_argument("--top", type=int, default=5)
with sqlite3.connect("app.db") as conn:
    conn.execute("SELECT * FROM t WHERE id = ?", (5,))
```

## Para ve güvenlik

```python
from decimal import Decimal, ROUND_HALF_UP
import hashlib, hmac, secrets
Decimal("19.99").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
key = hashlib.pbkdf2_hmac("sha256", b"pw", salt, 200_000)
hmac.compare_digest(a, b)
secrets.token_urlsafe(32)
```

## Eşzamanlılık

```python
from concurrent.futures import ThreadPoolExecutor
import asyncio
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch, urls))

async def main():
    async with asyncio.timeout(5):
        return await asyncio.gather(*(get(u) for u in urls))
```

## Test, ölçüm, bellek

```python
import unittest, timeit, cProfile, tracemalloc
class TestX(unittest.TestCase):
    def test_a(self):
        self.assertEqual(f(2), 4)

min(timeit.repeat(f, number=100, repeat=5))
cProfile.Profile().runcall(main)
tracemalloc.start(); snap = tracemalloc.take_snapshot()
```
