What's used most when testing an API with pytest.

## Commands (in a terminal)

| Command | What it does |
|---|---|
| `pytest` | Runs every `test_*.py` file in the folder |
| `pytest -q` | Short output |
| `pytest test_main.py` | One file |
| `pytest -k missing` | Tests with `missing` in their name |
| `pytest -x` | Stop at the first failure |

In your computer's environment you need `pip install pytest`; Odyssey's
exercise environment already has it.

## `assert` patterns

```python
assert r.status_code == 201
assert r.json() == {"id": 1, "title": "Dune", "year": 1965}   # all of it
assert r.json()["title"] == "Dune"                            # one field
assert "id" in r.json()                                       # field exists
assert len(r.json()) == 3                                     # list length
assert r.headers["location"] == "/books/1"                    # a header
```

For unknown values (a token, a time) test their presence or format rather
than all of it: `assert len(r.json()["access_token"]) == 32`.

## Fixtures

```python
@pytest.fixture
def client():
    return TestClient(app)


def test_home(client):          # parameter name = fixture name
    assert client.get("/").status_code == 200
```

A fixture without `autouse=True` is given only to tests that ask for it as a
parameter.

## Test names

`test_` + what's tried: `test_missing_book_returns_404`,
`test_duplicate_email_is_409`. When it fails, the reader understands what
broke from the name.

## Common mistakes

| Mistake | Result |
|---|---|
| The function name doesn't start with `test_` | pytest doesn't see it; "no tests" |
| `print` instead of `assert` | The test never fails |
| Tests don't clean shared state | The result depends on the order |
| `dependency_overrides` isn't cleared | Later tests run with the fake |
