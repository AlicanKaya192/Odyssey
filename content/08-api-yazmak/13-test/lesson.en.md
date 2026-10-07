# Testing an API

You changed an endpoint; how will you know you didn't break something
else? Trying every request by hand in `/docs` after every change is tiring
and easy to forget. Instead you write the requests and the expected
answers as **code**; one command runs them all in seconds. In this section
you write tests for the API with **pytest** and FastAPI's **TestClient**.

This is exactly what checks the exercises in Odyssey: behind every exercise
there are tests sending requests to your code. Now you're on the other side
of the table.

## The first test

Let `main.py` hold a book API. Next to it, `test_main.py`:

```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_book():
    r = client.post("/books", json={"title": "Dune", "year": 1965})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "Dune", "year": 1965}


def test_read_missing():
    r = client.get("/books/99")
    assert r.status_code == 404
    assert r.json()["detail"] == "Book not found"
```

- `TestClient(app)`: a client that calls the application **in the same
  process**, without starting a server. The same style as `requests` in
  API 1: `client.get`, `client.post(..., json=...)`, `r.status_code`,
  `r.json()`.
- Every function whose name starts with `test_` is a test. pytest finds them
  by itself.
- `assert condition`: if the condition is false, the test **fails**.

To run them, `pytest` in a terminal (in Odyssey, **Run** the exercise). When
they all pass:

```text
......                                                    [100%]
6 passed in 0.39s
```

Each dot is a passing test.

## What does a failing test look like?

```text
..F...                                                    [100%]
_____________________ test_first_id_again _____________________
    def test_first_id_again():
        r = client.post("/books", json={"title": "Emma", "year": 1815})
>       assert r.json()["id"] == 1
E       assert 2 == 1
FAILED test_main.py::test_first_id_again - assert 2 == 1
1 failed, 5 passed in 0.59s
```

pytest shows which line failed (`>`) and the values on both sides
(`2 == 1`). We measured this output (the rule lines were shortened to fit
the page); why it failed is under the next heading.

<figure class="fig">
  <div class="flow">
    <span class="node">test_main.py<br><small>client.post(...)</small></span><span class="arrow">→</span>
    <span class="node acc">TestClient<br><small>no server</small></span><span class="arrow">→</span>
    <span class="node">main.app</span><span class="arrow">→</span>
    <span class="node ok">assert<br><small>201? the right body?</small></span>
  </div>
  <figcaption>The tests call the application in the same process; every <code>assert</code> checks one expectation. If one doesn't hold, the test fails and pytest shows which line.</figcaption>
</figure>

## Tests mustn't affect each other

The test above would pass if it ran alone. It failed because the earlier
`test_add_book` had added Dune to the `books` dictionary, and the dictionary
is **shared** between tests. The result depended on the order: a bad test.

The fix: a **fixture** that cleans the state before every test:

```python
import pytest

from main import books


@pytest.fixture(autouse=True)
def clean():
    books.clear()
    yield
    books.clear()
```

- `@pytest.fixture`: a preparation function that runs before/after tests.
- `autouse=True`: applied to every test automatically.
- `yield`: like in dependencies; the part before runs before the test, the
  part after runs after it.

With the fixture, the same six tests give `6 passed` (we measured).

## The same test with many inputs: `parametrize`

```python
@pytest.mark.parametrize("body", [
    {"title": "X"},
    {"year": 1},
    {"title": "X", "year": "old"},
])
def test_bad_bodies(body):
    assert client.post("/books", json=body).status_code == 422
```

One function, three tests: pytest runs each input separately and reports it
separately. Trying boundary values (`0`, `1`, the largest, one more than the
largest) is easy this way.

## Swapping a dependency in a test

The `dependency_overrides` you saw in the Dependencies section helps in
tests:

```python
from main import app, require_key


def test_stats_without_real_key():
    app.dependency_overrides[require_key] = lambda: None
    try:
        assert client.get("/admin/stats").status_code == 200
    finally:
        app.dependency_overrides.clear()
```

Instead of the real key check you gave "always passes". The same way, an
empty temporary database is given instead of the real one. Clearing in
`finally` is a must; otherwise later tests run with the fake dependency too.

## What does a good test try?

| Try | Example |
|---|---|
| The happy path | `POST` → `201` and the right body |
| Not found | a missing number → `404` |
| Broken input | a missing field, a wrong type → `422` |
| Boundaries | `limit=0`, `limit=50`, `limit=51` |
| Identity | no key → `401`, wrong role → `403` |
| A flow | add → read → delete → read (`404`) |

A test must be **able to catch broken code**. Odyssey measures this too:
your tests are also run against a deliberately broken version of the
application; if they all still pass, it says "your tests don't see this
bug".

## Summary

- `TestClient(app)`: a serverless client; written like `requests`.
- `def test_...():` + `assert`; pytest finds and runs them.
- Shared state ties tests together: clean it with
  `@pytest.fixture(autouse=True)`.
- `@pytest.mark.parametrize`: the same test, many inputs.
- A fake dependency with `app.dependency_overrides`; then `clear()`.
- A good test tries the happy path and the errors, and fails on broken code.
