Turning a question into parameters: examples from the practice server.

| Question | `params` |
|---|---|
| All of Austen's books | `{"author": "Austen"}` |
| The 3 cheapest classics | `{"tag": "classic", "sort": "price", "per_page": 3}` |
| The newest science fiction | `{"tag": "scifi", "sort": "-year", "per_page": 1}` |
| 1900–1930, by year | `{"year_min": 1900, "year_max": 1930, "sort": "year"}` |
| Titles containing "dune" | `{"q": "dune"}` |
| Both science fiction and humour | `{"tag": ["scifi", "humor"]}` |

## The order for solving a question

1. **What do I want?** Which records (filtering), in which order (sorting),
   how many (limit)?
2. **Which parameter does the documentation offer?** The name and the value
   format (`sort=-year` or `order=desc`?).
3. **Send the request and look at `r.url`.** Is the address that went out
   the one you meant?
4. **Check the result.** Are the count and the order what you expected? What
   is `meta.total`?

## Filtering the server cannot do

The practice server does not filter by a price range (there is no
`price_max`). Then:

```python
params = {"tag": "classic", "per_page": 20}
books = requests.get(BASE + "/books", params=params).json()["data"]
cheap = [b for b in books if b["price"] < 10]
```

First narrow down as far as the server can (`tag=classic`), then filter the
rest in Python. That way you do not download more records than needed.
