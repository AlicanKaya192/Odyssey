Every case of building a query with `params=`.

| Dictionary | Query sent |
|---|---|
| `{"author": "Austen"}` | `?author=Austen` |
| `{"q": "the lighthouse"}` | `?q=the+lighthouse` |
| `{"q": "fish & chips"}` | `?q=fish+%26+chips` |
| `{"per_page": 3}` | `?per_page=3` |
| `{"tag": ["scifi", "humor"]}` | `?tag=scifi&tag=humor` |
| `{"author": "Orwell", "tag": None}` | `?author=Orwell` |
| `{}` | (no query) |

## Patterns

```python
r = requests.get(BASE + "/books", params={"author": "Austen", "sort": "-year"})
print(r.url)                     # check the address that went out
books = r.json()["data"]
if not books:
    print("nothing found")       # 200 + an empty list
```

Optional parameters:

```python
def search(**filters):
    return requests.get(BASE + "/books", params=filters).json()["data"]

search(author="Austen")
search(tag="scifi", sort="-year")
```

`**filters` gathers every named value given to the function into a
dictionary; that dictionary becomes `params` directly.

## When the address already has a query

```python
r = requests.get(BASE + "/books?sort=year", params={"tag": "scifi"})
print(r.url)   # .../books?sort=year&tag=scifi
```

requests adds the new parameters with `&`; it does not write a second `?`.
Still, keeping them in one place (only `params`) makes the code easier to
read.

## Remember

- Parameter names and meanings differ from API to API: `per_page`, `limit`,
  `size`, `pageSize`... Check the documentation.
- An API often ignores an unknown parameter without a word. If the result is
  not what you expected, compare the name in `r.url` with the documentation
  first.
